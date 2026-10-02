"""Rebuild/check the D1B CV4 design from main. Python standard library only."""
from pathlib import Path
import hashlib
import html
import json
import re
import sys
import argparse
from html.parser import HTMLParser

# --check must be read-only even when its regression helper is imported.
sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = HERE.parent
EVIDENCE = OUT / '证据'
BASE_MAIN = '567d9cd32befc2b8aa7ae99487f8b6d2170f1436'
CONTRACT_CANDIDATE = 'e8ad944e7c9c8df77c7c5fd883c4459a75270e92'
PR2_REVIEW_HEAD = 'f47fa3e251d5fa02f077a6cf9f39feeebf15d3f4'
HEADER_SHA = '73217a0db2469c4349c4b54bb97fd1d3ea88f01ca82285027b95d10bf3bf7161'
BASE_IDENTITY = {'base_main': BASE_MAIN, 'contract_candidate': CONTRACT_CANDIDATE,
                 'pr2_review_head': PR2_REVIEW_HEAD, 'contract_version': 4}
PENDING_INTERFACE_CONTROLS = {'P14-04','P15-04','D20-05','P30-19'}
BASELINES = {
    'docs/退休人员名册打印小程序需求说明.docx': '658b10952e2cba734990d2b37f862b2495196e51427c117cf2a4edde7992c641',
    'docs/退休人员名册打印小程序开发规划.docx': 'c1caac2094c6778363b27af2011af3cd0118fa4e96e570761479247748d347c1',
    'reference/七阶段开发任务清单.xlsx': '7648e936d249f817bc61d43bcf109eafc94802b9a1dfd370fd23cdb45d802e26',
    'reference/员工信息表11111.xlsx': '427727f5d8062e7cba699b35d9262fb594b717d3dd699f811cbb7475112cf5b6',
}

def write(path, value):
    path.write_text(value, encoding='utf-8')

def json_text(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'

def table(headers, rows):
    def safe(value):
        return str(value).replace('|', '／').replace('\n', '<br>')
    return '\n'.join(['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join(['---'] * len(headers)) + ' |'] +
                     ['| ' + ' | '.join(safe(cell) for cell in row) + ' |' for row in rows])

def enum_members(header, name):
    body = re.search(r'enum class ' + name + r'\s*:[^{]+\{(.*?)\};', header, re.S).group(1)
    body = re.sub(r'//[^\n]*', '', body)
    return [part.split('=')[0].strip() for part in body.split(',') if part.strip()]

def struct_members(header, name):
    body = re.search(r'struct ' + name + r'\s*\{(.*?)\};', header, re.S).group(1)
    body = re.sub(r'//[^\n]*', '', body)
    return re.findall(r'\b(\w+)\s*(?:=[^;]*)?;', body)

def function_body(header, signature):
    """Extract a balanced C++ body; nested switches must not truncate checks."""
    start = header.index('{', header.index(signature))
    depth = 1
    for end in range(start + 1, len(header)):
        depth += (header[end] == '{') - (header[end] == '}')
        if depth == 0:
            return header[start + 1:end]
    raise ValueError('Unbalanced contract function: ' + signature)

def explicit_mapping(header, enum):
    body = function_body(header, 'try_to_person_field(' + enum)
    pairs = re.findall(r'case ' + enum + r'::(\w+):\s*\*out = FieldId::(\w+);\s*return true;', body)
    names = [x for x in enum_members(header, enum) if x != 'Unspecified']
    return (len(pairs) == len(names) and len(set(a for a, _ in pairs)) == len(names)
            and dict(pairs) == {x: x for x in names}
            and 'Unspecified' not in dict(pairs) and 'default: return false;' in body
            and 'out == nullptr' in body)

def load_contract(header):
    pattern = r'\{FieldId::(\w+), "([^"]+)", FieldValueKind::(\w+), ((?:true|false)(?:, (?:true|false)){5})\}'
    flags = ['required_for_import', 'sensitive', 'source_importable', 'user_editable', 'system_managed', 'printable_by_default']
    fields = []
    for ident, key, kind, bits in re.findall(pattern, header):
        fields.append({'id': ident, 'key': key, 'value_kind': kind,
                       **dict(zip(flags, [bit == 'true' for bit in bits.split(', ')]))})
    return fields

def make_controls(data, fields):
    pages = data['pages']
    rows = []
    field_rows = []
    for index, field in enumerate(fields, 1):
        ident = field['id']
        cid = f'P22-F{index:02}'
        label = data['field_labels'][ident]
        readonly = field['system_managed']
        override = data['ui_overrides'].get(ident, {})
        condition = ('只读；服务生成' if readonly else
                     '仅编辑模式；新增只读，由服务初始化' if ident == 'PinyinSortKey' else
                     '新增按业务校验；既有只读，更正唯一入口D20，待Q04批准' if override.get('existing_readonly') else
                     '新增／编辑业务资料')
        validation = '服务负责，调用方不可填ID、固定编号或审计值' if readonly else '可空可重复，保留前导零，禁止作为身份唯一键' if ident == 'EmployeeNo' else '去首尾空格后非空；唯一导入必填' if ident == 'FullName' else '不可导入；编辑以FieldChange维护' if ident == 'PinyinSortKey' else '字段未改变不发送change；清空clear_value=true'
        if field['sensitive']:
            validation += '；默认脱敏、默认不打印；不回写掩码，替换需明确输入'
        if not readonly:
            validation += '；FieldChange.field=EditableFieldId；服务try_to_person_field显式映射再查FieldSpec；forged/unknown/Unspecified拒绝'
            if field['value_kind'] in ('Text', 'EnumCode'):
                validation += '；赋值用value，date_value=canonical Unknown；clear时value为空且日期全0'
            if override.get('ordinary_clear_allowed') is False:
                validation += '；UI禁止普通清空'
        if field['value_kind'] == 'Date':
            controls = [
                [cid, label+'精度', 'COMBOBOX CBS_DROPDOWNLIST', 'DatePrecision', 'Unknown／原精度', condition, 'Unknown全禁用；Year仅年；YearMonth年月；FullDate年月日；不补组件', '精度与组件不符，定位本字段'],
                [cid+'Y', label+'年', 'EDIT＋UPDOWN', 'DateValue.year', '空／原值；Unknown内部规范值为0', condition+'且Year/YearMonth/FullDate；Unknown disabled', '1–9999；不活动时空白且disabled', '年份不合法'],
                [cid+'M', label+'月', 'EDIT＋UPDOWN', 'DateValue.month', '空／原值；Unknown内部规范值为0', condition+'且YearMonth/FullDate；其余disabled', '1–12；不活动时空白且disabled', '月份不合法'],
                [cid+'D', label+'日', 'EDIT＋UPDOWN', 'DateValue.day', '空／原值；Unknown内部规范值为0', condition+'且FullDate；其余disabled', '真实日历含闰日；不活动组件空白，DTO为0；提交date_value', '日期不合法，不补成每月1日'],
            ]
            validation = '日期赋值clear=false/value为空/date_value有效且已知；清空clear=true/value为空/canonical Unknown；Unknown UI空白且disabled，内部为0；服务显式映射EditableFieldId'
            if override.get('existing_readonly'):
                validation += '；既有只读，仅D20更正；P22禁止普通清空'
        else:
            kind = 'STATIC' if readonly else 'COMBOBOX CBS_DROPDOWNLIST' if field['value_kind'] == 'EnumCode' else 'EDIT ES_MULTILINE' if ident in ('HomeAddress','Remark') else 'EDIT'
            controls = [[cid,label,kind,'维护'+field['key'],'保存后生成／服务现值' if readonly else '空／原值',condition,validation,'读取失败提示' if readonly else '校验失败保留草稿并定位字段']]
        rows.extend(controls)
        field_rows.append({**field,'label':label,'control_ids':[r[0] for r in controls], 'ui_rule':condition,'validation':validation,'ui_override':override})
    rows += [
        ['P22-01','保存业务资料','BUTTON','新增用PersonCreateInput；编辑用PersonEditInput，不提交Tag或系统字段','可用','当前业务输入有效','不改与清空区分；新增不含初始拼音','备份／校验／冲突失败保留草稿'],
        ['P22-02','取消','BUTTON','有草稿D90后回来源页','可用','未执行写入','按取消路径','保存失败留编辑页'],
        ['P22-T01','标签列表','SysListView32 LVS_REPORT','读取与P30相同TagRecord来源','未选择','人员已保存','代码、值、适用年及审计只读列表','加载失败保留现值并标未更新'],
        ['P22-T02','标签代码','COMBOBOX CBS_DROPDOWNLIST','TagMutation.tag_code','未选择','人员已保存','A/R字典代码；不包含派生高龄','标签代码不合法'],
        ['P22-T03','标签值','EDIT','TagMutation.tag_value','空／原值','人员已保存','按字典值域','标签值不合法'],
        ['P22-T04','适用年','EDIT＋UPDOWN','TagMutation.applicable_year','0或选中标签年份','人员已保存','0常年；年度慰问必须具体年份，不跨年沿用','请明确年度慰问适用年'],
        ['P22-T05','添加／修改标签','BUTTON','UpdateTagRequest，remove=false，changed_by来自OperatorContext','可用','人员已保存且TagMutation有效','独立请求，updated_at/updated_by由服务生成','失败保留标签草稿，不冒充业务字段已失败'],
        ['P22-T06','删除标签','BUTTON','UpdateTagRequest，remove=true','按选择','已选标签且明确确认','匹配代码及适用年；服务审计','删除失败保留标签'],
        ['P22-T07','标签审计','STATIC','TagRecord.updated_at／updated_by','读取值','只读','不可直接提交审计值','读取失败提示'],
    ]
    pages['P22'] = {'name':'业务资料、独立Tag与只读系统区','controls':rows}
    return [row for page in pages.values() for row in page['controls']], field_rows

def template_sections(templates):
    sections, layouts = [], []
    for template in templates:
        width, height = (2970,2100) if template['orientation']=='Landscape' else (2100,2970)
        margins = template['margins']
        available_width = width-margins['left_tenth_mm']-margins['right_tenth_mm']
        available_height = height-margins['top_tenth_mm']-margins['bottom_tenth_mm']
        used_width = sum(c['width_tenth_mm'] for c in template['columns'] if c['visible'])
        used_height = 400 + template['rows_per_page']*template['row_height_tenth_mm']
        layouts.append({'template_id':template['template_id'],'unit':'0.1mm','used_width':used_width,'available_width':available_width,'used_height':used_height,'available_height':available_height,'pass':used_width<=available_width and used_height<=available_height,'scope':'仅作者建议预留的算术；硬边距/字体/转换未验收'})
        params = [
            ['ID／版本／状态',f"{template['template_id']}／{template['template_version']}／{template['status']}"],
            ['名称／标题',template['template_name']+'／'+template['title']+'（变量来自快照，先解析）'],
            ['纸张／方向',f"A4／{template['orientation']}／{width}×{height}（0.1mm）"],
            ['正文／标题／表头字号pt',f"{template['font_size_pt']}／{template['title_font_size_pt']}／{template['header_font_size_pt']}"],
            ['四边距0.1mm','左150／右150／上150／下150；UI均15mm'],
            ['行高／每页人数',f"{template['row_height_tenth_mm']}（0.1mm）／{template['rows_per_page']}；0另表示自动计算"],
            ['repeat_header／page_number_policy',f"{template['repeat_header']}／{template['page_number_policy']}"],
            ['签字／备注','签字为BlankSignature列；无全局开关；需要人员备注时另添PersonField::Remark'],
            ['宽高算术',f'{used_width}≤{available_width}；{used_height}≤{available_height}（0.1mm）；硬边距/字体/换行仍待验证'],
            ['名单来源','同snapshot_id；不重新筛选、不重算派生值；连续打印序号'],
        ]
        columns = [[i+1,c['display_name'],c['source'],c['field'] or c['derived_field'] or '空白签字',c['width_tenth_mm'],c['width_tenth_mm']/10,'是' if c['visible'] else '否'] for i,c in enumerate(template['columns'])]
        sections.append(f"### {template['template_id']} {template['template_name']}\n\n"+table(['参数','建议值／说明'],params)+'\n\n'+table(['序','display_name','source','活动成员','宽0.1mm','UI毫米','visible'],columns))
    return '\n\n'.join(sections), layouts

def check_row(name, passed, detail):
    return {'check':name,'pass':bool(passed),'detail':detail}

def local_links(md):
    return [link for link in re.findall(r'\[[^\]]+\]\(([^)]+)\)', md) if not link.startswith(('https://','#'))]

def inline(value):
    value = html.escape(value)
    value = re.sub(r'`([^`]+)`',r'<code>\1</code>',value)
    def link(match):
        label,url=match.groups()
        if url.startswith(('../','../../')):
            target=(OUT/url).resolve().relative_to(ROOT).as_posix()
            from urllib.parse import quote
            url='https://github.com/gaoyizhe934/retiree-roster-win7/blob/'+BASE_MAIN+'/'+quote(target)
        return '<a href="'+url+'">'+label+'</a>'
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)',link,value).replace('&lt;br&gt;','<br>')

def render_md(md):
    lines=md.splitlines(); parts=[]; toc=[]; i=0; heading=0
    while i<len(lines):
        line=lines[i]
        if line.startswith('```'):
            lang=line[3:]; i+=1; block=[]
            while i<len(lines) and not lines[i].startswith('```'):
                block.append(lines[i]); i+=1
            text='<pre><code>'+html.escape('\n'.join(block))+'</code></pre>'
            if lang=='mermaid': text=flow_svg()+'<details><summary>完整 Mermaid 图源</summary>'+text+'</details>'
            parts.append(text)
        elif line.startswith('#'):
            match=re.match(r'(#+) (.*)',line)
            if match:
                level=len(match[1]); heading+=1; anchor=f'section-{heading}'
                parts.append(f'<h{level} id="{anchor}">{inline(match[2])}</h{level}>')
                if level==2: toc.append(f'<a href="#{anchor}">{inline(match[2])}</a>')
        elif line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].startswith('|'):
                cells=lines[i].strip().strip('|').split('|')
                if not all(re.fullmatch(r'\s*:?-+:?\s*',cell) for cell in cells): rows.append(cells)
                i+=1
            table_class = ' class="controls-table"' if len(rows[0])==8 and rows[0][0].strip()=='编号' else ''
            parts.append('<div class="table-scroll" tabindex="0" role="region" aria-label="'+html.escape(' / '.join(c.strip() for c in rows[0]))+'"><table'+table_class+'><thead><tr>'+''.join('<th>'+inline(c.strip())+'</th>' for c in rows[0])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+inline(c.strip())+'</td>' for c in row)+'</tr>' for row in rows[1:])+'</tbody></table></div>')
            continue
        elif line.strip(): parts.append('<p>'+inline(line)+'</p>')
        i+=1
    return '\n'.join(parts),'\n'.join(toc)

def flow_svg():
    labels=['本地操作员／首页','P10 文件与 P11 表头','P12 Profile与逐列处置','P13 预检身份／revision','P14 问题与重复候选','D10 确认当前预检','P15 事务／失败重预检','P20／P21 人员详情','P22 业务／独立Tag','P30 显式条件→快照','P40／P41 模板值副本','P50 同快照预览','D50 打印／D51 xlsx','P51 本地反馈／脱敏']
    positions=[(25+(i%3)*260,25+(i//3)*125) for i in range(len(labels))]
    result=['<svg viewBox="0 0 810 700" role="img" aria-label="D1B主路径与快照流程"><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" fill="#487174"/></marker></defs>']
    for i in range(len(labels)-1):
        x,y=positions[i];xx,yy=positions[i+1]
        path=f'M{x+225},{y+32} L{xx},{yy+32}' if y==yy else f'M{x+112},{y+65} L{x+112},{y+95} L{xx+112},{y+95} L{xx+112},{yy}'
        result.append(f'<path d="{path}" fill="none" stroke="#487174" stroke-width="2" marker-end="url(#arrow)"/>')
    for label,(x,y) in zip(labels,positions):
        result.append(f'<rect x="{x}" y="{y}" width="225" height="65" rx="8" fill="#edf4ef" stroke="#789c97"/><text x="{x+112}" y="{y+39}" text-anchor="middle" font-size="16" fill="#183d39">{label}</text>')
    result.append('<text x="25" y="682" font-size="14">阶段概览；问题页可选，分支与取消／StaleSnapshot返回详见完整图与路径表。</text></svg>')
    return ''.join(result)

def make_html(md):
    body,toc=render_md(md)
    css='''body{margin:0;background:#f4f5f3;color:#22352f;font:17px/1.75 "Microsoft YaHei",sans-serif}aside{position:fixed;top:0;bottom:0;width:225px;background:#e6ece7;padding:20px;overflow:auto}aside strong{display:block;margin-bottom:16px}aside a{display:block;margin:12px 0;color:#25463b;text-decoration:none;font-size:15px}main{margin-left:265px}header{padding:25px 38px;background:#203d36;color:white}article{padding:26px 38px;max-width:1600px}h1{font-size:30px}h2{font-size:25px;margin-top:44px;padding-top:20px;border-top:2px solid #c4d5cb;scroll-margin-top:15px}h3{font-size:21px;margin-top:30px}p{max-width:1080px}a{color:#176650}code{font-family:Consolas,"Microsoft YaHei",monospace;background:#e9eeea;padding:1px 4px}pre{background:#f8faf8;border:1px solid #cad8cf;padding:20px;overflow:auto;line-height:1.65;font-size:15px}pre code{background:none;padding:0}.table-scroll{overflow:auto;margin:20px 0}table{border-collapse:collapse;width:100%;min-width:850px;font-size:15px}th,td{padding:11px 12px;border:1px solid #cad8cf;vertical-align:top;text-align:left}th{background:#dfeae3}tbody tr:nth-child(even){background:#edf3ed}td:first-child{white-space:nowrap}svg{width:100%;max-width:1050px;height:auto}details{margin:15px 0}@media(max-width:1000px){aside{position:static;width:auto}aside a{display:inline-block;margin:5px 12px}main{margin:0}article{padding:20px}}@media print{aside{display:none}main{margin:0}header{background:white;color:black}body{background:white}article{padding:0}.table-scroll{overflow:visible}table{min-width:0;font-size:9pt}h2,h3{break-after:avoid}tr{break-inside:avoid}details{display:none}}'''
    css += '''.table-scroll:focus-visible{outline:3px solid #176650;outline-offset:3px}.controls-table{table-layout:fixed;width:1940px;min-width:1940px}.controls-table th:nth-child(1){width:90px}.controls-table th:nth-child(2){width:130px}.controls-table th:nth-child(3){width:185px}.controls-table th:nth-child(4){width:290px}.controls-table th:nth-child(5){width:190px}.controls-table th:nth-child(6){width:265px}.controls-table th:nth-child(7){width:390px}.controls-table th:nth-child(8){width:200px}.controls-table td{overflow-wrap:anywhere}@media print{.controls-table{width:100%;min-width:0;table-layout:auto}.controls-table th:nth-child(n){width:auto}.controls-table td:first-child{white-space:normal}.controls-table td{overflow-wrap:anywhere}}'''
    return '<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>D1B 契约v4设计</title><style>'+css+'</style></head><body><aside><strong>D1B v0.3 复核材料</strong>'+toc+'</aside><main><header>ContractVersion 4 · Draft · Gate 0 未通过<br>作者静态设计证据；模板参数待甲方确认；非作者R未签认</header><article>'+body+'</article></main></body></html>'

class Structure(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=set(); self.links=[]; self.tables=0; self.svg=0; self.external=[]; self.headings=[]; self.text=[]; self.heading=None
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if 'id' in attrs: self.ids.add(attrs['id'])
        if tag=='a': self.links.append(attrs.get('href',''))
        if tag=='table': self.tables+=1
        if tag=='svg': self.svg+=1
        if tag in ('script','link','img','iframe') and (attrs.get('src') or attrs.get('href')): self.external.append(attrs)
        if re.fullmatch(r'h[1-6]',tag): self.heading=[]
    def handle_endtag(self,tag):
        if re.fullmatch(r'h[1-6]',tag) and self.heading is not None:
            self.headings.append(''.join(self.heading)); self.heading=None
    def handle_data(self,data):
        self.text.append(data)
        if self.heading is not None: self.heading.append(data)

def static_checks(header,md,data,fields,tabs,layouts):
    controls=data['controls']; ids=[c[0] for c in controls]; templates=data['templates']
    tag_controls=[c for c in controls if c[0].startswith('P22-T')]
    imports=set(data['import_fields']); editable=set(data['editable_fields']); system={f['id'] for f in fields if f['system_managed']}
    checks=[]
    def check(name,passed,detail): checks.append(check_row(name,passed,detail))
    check('34字段与契约枚举完整一致',len(fields)==34 and [f['id'] for f in fields]==enum_members(header,'PersonFieldId'),'FieldSpec与PersonFieldId逐项及顺序核对')
    check('字段能力由契约解析',imports=={f['id'] for f in fields if f['source_importable']} and editable=={f['id'] for f in fields if f['user_editable']},'ImportFieldId/EditableFieldId与source_importable/user_editable一致')
    check('系统字段边界',system=={'PersonId','PersonCode','CreatedAt','UpdatedAt','ImportBatchId','LastModifiedBy'} and not(imports&system) and not(editable&system),'6个系统专管字段无导入和编辑入口')
    check('拼音创建与编辑边界','PinyinSortKey' not in imports and 'PinyinSortKey' in editable and 'PinyinSortKey' not in system and 'pinyin_sort_key' not in struct_members(header,'PersonCreateInput'),'服务初始化、禁止导入、后续可编辑')
    check('唯一导入必填', [f['id'] for f in fields if f['required_for_import']]==['FullName'],'LifeStatus必须解析，独立于required_for_import元数据')
    check('PersonId/PersonCode/工号三分离',all(x in {f['id'] for f in fields} for x in ('PersonId','PersonCode','EmployeeNo')) and '工号，可空、可重复' in md and 'PersonCode 是业务可见固定编号' in md,'工号不作为内部ID或固定编号')
    check('Person输入不收系统字段',not(set(struct_members(header,'PersonCreateInput')) & {f['key'] for f in fields if f['system_managed']}),'新增仅PersonCreateInput，编辑仅FieldChange/EditableFieldId')
    check('Tag不混入Person',not({'TagCodes','IsHighAgeMarked','CareFlags'}&{f['id'] for f in fields}) and 'TagMutation' in md and len(tag_controls)==7,'独立代码、值、适用年、添加修改删除、只读审计')
    check('Tag年度与审计边界',set(struct_members(header,'TagMutation'))=={'tag_code','tag_value','applicable_year','remove'} and '不跨年继承' in md and tag_controls[-1][2]=='STATIC','updated_at/updated_by无提交入口；高龄不持久化')
    check('日期精度覆盖',sum(f['value_kind']=='Date' for f in fields)==6 and all(len(f['control_ids'])==4 for f in fields if f['value_kind']=='Date') and '不能参与比较' in md,'六个DateValue字段各有精度与年月日组件；未知不为0年龄')
    check('全列三种处置',enum_members(header,'ImportColumnDisposition')==['PersonField','BatchRawOnly','Unsupported'] and all(x in md for x in ('BatchRawOnly','目标必须 Unspecified','Unsupported 是默认')),'默认Unsupported；BatchRawOnly本机原值不进Person或公共日志')
    check('无冻结Profile自动直入', '当前没有已冻结 Profile' in md and '唯一匹配已冻结 Profile 且无缺失、重复、歧义、顺序变化、未知列' in md,'仅已冻结唯一匹配可预填；所有路径预检')
    check('确认仅绑定revision',set(struct_members(header,'ConfirmImportRequest'))=={'meta','batch_id','preview_revision','confirmed_by'} and all(x in md for x in ('成功revision不可重复确认','mapping_version','immutable checked copy')),'预检不可变，变化获得新revision，确认无第二套语义')
    check('FilterSpec全能力',enum_members(header,'RosterScenario')==['Custom','Chongyang','Party50'] and all(x in md for x in ('as_of_date','accepted_values','has_minimum','field_match','tag_match','require_party_member','Unspecified不能被当成LivingOnly')),'三场景、显式状态、年龄口径、集合/下限、两组All/Any、八种比较')
    check('无最大年龄输入',not any(c[1]=='最大年龄' or c[3].endswith('.maximum') for c in controls if c[0].startswith('P30-')) and 'maximum' not in struct_members(header,'YearCountCondition'),'当前只有集合与含边界下限')
    check('P40/P50消费快照',all('snapshot_id' in ' '.join(str(r) for r in data['pages'][pid]['controls']) for pid in ('P40','P50')) and all('snapshot_id' in struct_members(header,name) and 'filter' not in struct_members(header,name) for name in ('PreviewRosterRequest','PrintRosterRequest','ExportRosterRequest')),'三输出不再接收FilterSpec')
    check('快照失效范围',all(x in md for x in ('StaleSnapshot','人员、Tag、拼音键、导入、恢复、迁移','恢复不能复用旧版本号','同一临界区')),'失效禁输出，回P30；不会混入新数据')
    check('T03编号与派生列',any(c['field']=='PersonCode' for c in templates[2]['columns']) and not any(c['field']=='PersonId' for c in templates[2]['columns']) and any(c['derived_field']=='PartySeniorityYears' for c in templates[2]['columns']),'固定编号PersonCode；年度年龄及党龄从快照读取')
    check('模板契约与来源',all(set(struct_members(header,'PrintTemplate'))<=set(t) for t in templates) and all(c['source'] in enum_members(header,'TemplateColumnSource') for t in templates for c in t['columns']),'模板所有成员、四来源；候选JSON另有status说明')
    check('签字是独立列',all(any(c['source']=='BlankSignature' for c in t['columns']) for t in templates) and all('add_signature_column' not in t for t in templates),'统一columns[]，无第二个签字开关')
    check('物理尺寸整数与人数语义',all(isinstance(t['row_height_tenth_mm'],int) and all(isinstance(v,int) for v in t['margins'].values()) and all(isinstance(c['width_tenth_mm'],int) for c in t['columns']) for t in templates) and 'rows_per_page=0' in md,'内部0.1mm，UI毫米转换，正数人数校验')
    check('模板算术范围',all(c['pass'] for c in layouts),json.dumps(layouts,ensure_ascii=False))
    check('控件编号及八项记录',len(ids)==len(set(ids)) and all(len(c)==8 and all(str(v).strip() for v in c) for c in controls),f'{len(controls)}项；全部编号、名称、类型、用途、默认、启用、校验、错误')
    interactive={c[0] for c in controls if c[2] not in ('STATIC','msctls_progress32') and c[0] not in PENDING_INTERFACE_CONTROLS}
    check('Tab覆盖操作控件',interactive=={cid for row in tabs for cid in row['control_ids']+row.get('create_only_control_ids',[])},f'{len(interactive)}项，创建/编辑模式分开；日期组件只在活动精度启用时停靠')
    r_rows=re.findall(r'^\| RV\d{2}.*\| 待 R 复核 \|$',md,re.M)
    check('当前Draft与R未代签',len(r_rows)==9 and 'ContractVersion 4' in md and 'DatabaseSchemaVersion 独立且尚未分配' in md and 'Gate 0 未通过' in md,'九脚本待R，契约与数据库版本分开，未声明Gate通过')
    check('当前main契约指纹',hashlib.sha256(header.encode('utf-8')).hexdigest()==HEADER_SHA,'固定main的UTF-8文本SHA-256；不声称冻结Schema')
    for path,digest in BASELINES.items(): check('原始资料指纹：'+Path(path).name,hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,'与PR2原始文件基线一致，路径为仓库相对位置')
    check('CV4版本与基线身份',re.search(r'kCurrentContractVersion\s*=\s*4U',header) and data['contract_version']==4 and BASE_MAIN in md and 'ContractVersion 3' not in md and '279a204' not in md and 'PR2尚未合并' not in md,'main、contract candidate和PR2 review head分别记录')
    for enum,count in (('ImportFieldId',27),('EditableFieldId',28)):
        check(enum+'显式映射完整',len(enum_members(header,enum))==count+1 and explicit_mapping(header,enum),f'{count}个命名case；Unspecified/forged/default拒绝；nullptr保护')
    check('UI不依赖枚举数值identity',all(x in md for x in ('不允许整数 cast 成 PersonFieldId','不依赖 enum 数值 identity','forged／unknown／Unspecified','try_to_person_field(EditableFieldId')),'UI提交输入域枚举，服务显式映射后查询FieldSpec')
    change = function_body(header,'is_valid_field_change(')
    check('FieldChange日期payload', 'return change.value.empty() && change.date_value.is_known();' in change and all(x in md for x in ('日期赋值','有效且已知的 Year','Text／Enum 赋值混入日期均拒绝')),'Date不得用文本或非规范Unknown作赋值')
    check('FieldChange文本枚举payload','case FieldValueKind::Text:' in change and 'case FieldValueKind::EnumCode:' in change and 'return empty_date;' in change and '使用 value' in md,'Text/Enum必须canonical Unknown date，业务值域仍待D3')
    check('clear规范Unknown', 'if (change.clear_value) { return change.value.empty() && empty_date; }' in change and 'DatePrecision::Unknown' in change and 'change.date_value.is_valid()' in change and '年月日全0' in md,'clear必须空文本+规范未知；Identifier/Timestamp不可编辑')
    by_field={f['id']:f for f in fields}
    check('FullName禁止UI清空',by_field['FullName']['ui_override'].get('ordinary_clear_allowed') is False and 'UI禁止普通清空' in by_field['FullName']['validation'],'结构检查不代替必填业务验证')
    check('既有状态日期单入口',all(by_field[f]['ui_override'].get('existing_readonly') is True and by_field[f]['ui_override'].get('correction_route')=='D20' for f in ('LifeStatus','DeathDate')) and by_field['LifeStatus']['ui_override'].get('ordinary_clear_allowed') is False and 'D20 确认默认禁用' in md,'新建按业务校验，既有只读；更正待Q04批准')
    roster_members=struct_members(header,'RosterResult')
    check('RosterResult没有可写人数','total_count' not in roster_members and re.search(r'std::size_t total_count\(\) const\s*\{\s*return rows.size\(\);\s*\}',header),'total_count()只从rows.size()派生')
    check('人数UI派生读取',all('total_count()' in ' '.join(c) for p in ('P30','P40','P50') for c in data['pages'][p]['controls'] if c[0] in ('P30-35','P40-02','P50-01')) and '不存在第二份可写人数状态' in md,'P30/P40/P50无独立人数状态')
    year=function_body(header,'is_valid_year_count_condition(')
    check('YearCount空启用拒绝','condition.accepted_values.empty() && !condition.has_minimum' in year and 'enabled=true空集合无minimum' in md,'空集合且无下限不合法，关闭不约束')
    check('YearCount负值拒绝', 'condition.minimum < 0' in year and 'if (value < 0)' in year and '即使 has_minimum=false' in md,'enabled时minimum及每个accepted值均非负')
    check('YearCount仅shape','is_valid_year_count_condition()' in md and '不是完整 FilterSpec validator' in md,'target_year/as_of_date/status/scenario/field/tag由D4完整验证')
    check('预检caller proposal边界',all(x in md for x in ('caller proposal','Application Service 自己读取源文件','approved Profile','重复 Person target','可信 mapping_version','immutable checked data copy')),'P12调用方版本和配置不构成可信批准证据')
    check('Confirm源身份与checked copy',all(x in md for x in ('可重读源字节验证 SHA/identity','入库只消费 immutable checked copy','源缺失或变化必须拒绝')) and '确认不重读原文件' not in md and '不能重读可能已变化' not in md,'源重读仅验证身份，禁止替换已检数据')
    allow=set(data['filterable_fields'])
    excluded=system|{'NationalId','Phone','RelativePhone','HomeAddress','PersonCode','EmployeeNo','Remark'}
    check('筛选白名单排除系统敏感',bool(allow) and allow<={f['id'] for f in fields} and not allow&excluded and all(by_field[x]['value_kind'] in ('Text','EnumCode') for x in allow),'候选白名单待A/R；编号/工号精确与日期范围待决定')
    check('按类型限定Comparison',data['filter_comparisons']=={'EnumCode':['Equals','NotEquals'],'Text':['Equals','NotEquals','Contains','IsEmpty','IsNotEmpty'],'Date':[]},'契约比较全集不自动开放UI')
    dates=[c for c in controls if c[3] in ('DateValue.year','DateValue.month','DateValue.day')]
    check('Unknown日期UI空白',len(dates)==21 and all(c[4].startswith('空／原值') and 'disabled' in ' '.join(c) for c in dates),'18个Person组件与3个D20组件；Unknown不显示0')
    reports=[c for c in controls if c[0] in ('P14-04','P15-04')]
    check('未闭环报告默认禁用',len(reports)==2 and all(c[4].startswith('禁用') and 'D3接口对齐' in c[4] for c in reports),'Q11待定方式/格式/ExportLog/脱敏，B不增正式接口')
    search=next(c for c in controls if c[0]=='P20-01')
    check('搜索语义候选待确认','候选UI语义' in search[3] and '待A/R确认' in search[3] and '空 search_text' in md,'不从search_text推定字段匹配与排序')
    return checks

def delivery_checks(md,html_doc,data,all_public):
    doc=Structure(); doc.feed(html_doc); checks=[]
    def check(name,passed,detail): checks.append(check_row(name,passed,detail))
    md_headings=re.findall(r'^#{1,6} (.*)$',md,re.M)
    check('MD/HTML全部标题一致',md_headings==doc.headings,f'{len(md_headings)}个标题同序同文')
    anchors=[url[1:] for url in doc.links if url.startswith('#')]
    check('九章目录全部可定位',len(anchors)==9 and all(a in doc.ids for a in anchors),'九个正文主章节')
    check('离线资源',not doc.external,'无外部JS/CSS/图片/iframe；基线资料链接需联网，内容无需联网')
    check('表格与SVG完整',doc.tables==len(re.findall(r'^\| ---',md,re.M)) and doc.svg==1,f'{doc.tables}张表与1张阶段SVG，完整Mermaid图源可展开')
    text=''.join(doc.text)
    check('34字段与Tag完整显示',all(f['id'] in text and all(cid in text for cid in f['control_ids']) for f in data['fields']) and all(f'P22-T{i:02}' in text for i in range(1,8)),'全部字段能力、日期组件、独立Tag控件')
    check('Q/RV/T完整',all(f'Q{i:02}' in text for i in range(1,14)) and all(f'RV{i:02}' in text for i in range(1,10)) and all(t['template_id'] in text for t in data['templates']),'13对接项、9复核脚本、3模板')
    check('文档本地链接有效',all((OUT/url).exists() for url in local_links(md)),'生成稿链接按输出目录解析；HTML基线链接固定到main提交')
    check('无未替换占位符','<!--' not in md,'控件/字段/Tab/模板/静态检查均已生成')
    check('公共材料无私有绝对路径',not re.search(r'(?i)(?:(?<![a-z])[a-z]:[\\/]|file://|\\\\[^\s]+\\)',all_public),'README、正文、HTML、交接、修改报告及JSON证据全量扫描；HTTPS不误判为盘符')
    check('公共材料无真实敏感值',not re.search(r'(?<!\d)\d{17}[0-9Xx](?!\d)|(?<!\d)1[3-9]\d{9}(?!\d)',all_public),'无完整证号或大陆手机号；没有导入人员原值')
    check('未虚报功能/Gate', '待非作者 R 复核' in md and '代码／VM／事务／GDI／xlsx版式及实物未运行' in md and 'Gate 0 未通过' in md,'仅作者静态证据，非产品兼容验收')
    check('三模板全值同步',all(str(c['width_tenth_mm']) in text and c['display_name'] in text and c['source'] in text for t in data['templates'] for c in t['columns']),'MD/HTML由同一JSON模板源渲染')
    check('长表阅读与键盘横移',html_doc.count('class="controls-table"')==len(data['pages']) and 'width:1940px' in html_doc and 'tabindex="0" role="region"' in html_doc,'控件表有明确列宽，滚动区可键盘聚焦；打印恢复100%宽度')
    check('正式设计无内部技能术语',not any(x in md for x in ('ask-matt','beginning-work')) and '设计日期：2026-10-01' in md and '最后修订：2026-10-02' in md,'设计与修订日期分离')
    return checks

def generate_products():
    """Pure rebuild: return exact output bytes without touching deliverables."""
    header=(ROOT/'include/retiree_roster/schema_types.hpp').read_text(encoding='utf-8')
    data=json.loads((HERE/'设计数据.json').read_text(encoding='utf-8'))
    fields=load_contract(header)
    controls,field_rows=make_controls(data,fields)
    data.update({**BASE_IDENTITY,'status':'Draft; Gate 0 未通过','fields':field_rows,'controls':controls,
                 'import_fields':[x for x in enum_members(header,'ImportFieldId') if x!='Unspecified'],
                 'editable_fields':[x for x in enum_members(header,'EditableFieldId') if x!='Unspecified']})
    tabs=[]; sections=[]
    for pid,page in data['pages'].items():
        sections.append('### '+pid+' '+page['name']+'\n\n'+table(['编号','名称','Win32类型','用途','默认','启用条件','校验','错误提示'],page['controls']))
        visible=[r for r in page['controls'] if r[2] not in ('STATIC','msctls_progress32') and r[0] not in PENDING_INTERFACE_CONTROLS and not (pid=='P22' and '既有只读' in r[5])]
        initial={'P22':'P22-F04','D10':'D10-01','D20':'D20-06','D90':'D90-03','P15':'页面容器；执行完成后聚焦可用按钮'}.get(pid,visible[0][0] if visible else '页面容器')
        create_only=[r[0] for r in page['controls'] if pid=='P22' and r[2] not in ('STATIC','msctls_progress32') and '既有只读' in r[5]]
        tabs.append({'page':pid,'initial_focus':initial,'control_ids':[r[0] for r in visible], 'create_only_control_ids':create_only,
                     'dynamic_rule':'新建将create_only项按控件编号插回原位置；Unknown年月日/只读/禁用项跳过；列出的条件组件仅启用时停靠',
                     'enter':'多行仅换行；其余焦点按钮或安全查询／下一步；确认需明确聚焦','esc':'按§2取消；写入中等待'})
    data['tabs']=tabs
    templates,layouts=template_sections(data['templates'])
    md=(HERE/'设计正文.md').read_text(encoding='utf-8')
    # Source lives one level below final docs; normalize links when generating.
    md=re.sub(r'(\]\()\.\./',r'\1',md)
    # Pin baseline URLs so the standalone reading copy resolves its references.
    def baseline_link(match):
        label,url=match.groups()
        if url.startswith('../'):
            from urllib.parse import quote
            target=(OUT/url).resolve().relative_to(ROOT).as_posix()
            url='https://github.com/gaoyizhe934/retiree-roster-win7/blob/'+BASE_MAIN+'/'+quote(target)
        return '['+label+']('+url+')'
    md=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',baseline_link,md)
    yes=lambda value:'是' if value else '否'
    replacements={
        '<!-- CONTROLS -->':'\n\n'.join(sections),
        '<!-- FIELDS -->':table(['FieldId','契约键／类型','名称／控件','导入必填','敏感','source_importable','user_editable','system_managed','默认打印','UI条件／校验'],
            [[f['id'],f["key"]+'／'+f['value_kind'],f['label']+'／'+','.join(f['control_ids']),*[yes(f[k]) for k in ('required_for_import','sensitive','source_importable','user_editable','system_managed','printable_by_default')],f['ui_rule']+'；'+f['validation']] for f in field_rows]),
        '<!-- TAB -->':table(['页面','初始焦点','Tab候选顺序，Shift+Tab逆序','模式与精度规则','Enter','Esc'],[[r['page'],r['initial_focus'],' → '.join(r['control_ids']),r['dynamic_rule']+'；仅新建：'+','.join(r['create_only_control_ids']),r['enter'],r['esc']] for r in tabs])+ '\n\nD50／D51／文件／覆盖／帮助／历史：系统原生Tab顺序，默认取消，返回触发控件。',
        '<!-- TEMPLATES -->':templates,
    }
    for placeholder,value in replacements.items(): md=md.replace(placeholder,value)
    checks=static_checks(header,md,data,field_rows,tabs,layouts)
    md=md.replace('<!-- VALIDATION -->',table(['作者检查','结果','范围'],[[r['check'],'通过' if r['pass'] else '失败',r['detail']] for r in checks]))
    html_doc=make_html(md)
    products={
        OUT/'D1B_使用流程与模板设计.md':md,
        OUT/'D1B_使用流程与模板设计.html':html_doc,
        EVIDENCE/'控件与模板数据.json':json_text(data),
        EVIDENCE/'静态核查结果.json':json_text({**BASE_IDENTITY,'schema_sha256':HEADER_SHA,'status':'Draft','checks':checks,'layout':layouts}),
    }
    public=[md,html_doc,json_text(data),json_text(checks)]
    for name in ('README.md','D1B_交付与审核记录.md','D1B_评审修改报告.md'):
        if (OUT/name).exists(): public.append((OUT/name).read_text(encoding='utf-8'))
    deliveries=delivery_checks(md,html_doc,data,'\n'.join(public))
    import test_build_design
    negative = test_build_design.negative_results(sys.modules[__name__])
    products[EVIDENCE/'生成器反例核查结果.json']=json_text({'scope':'当前生成器的故意损坏输入反例，非C++/产品测试','checks':negative})
    inputs={}
    for path in (HERE/'设计正文.md',HERE/'设计数据.json',HERE/'build_design.py',HERE/'test_build_design.py',OUT/'README.md',OUT/'D1B_交付与审核记录.md',OUT/'D1B_评审修改报告.md',ROOT/'include/retiree_roster/schema_types.hpp'):
        inputs[path.relative_to(ROOT).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
    products[EVIDENCE/'交付核查结果.json']=json_text({**BASE_IDENTITY,'checked_input_sha256':inputs,
        'head_sha':None,'merge_base_sha':BASE_MAIN,'review_head_source':'PR #3 当前head及提交后发布快照','validation_subject':'当前CV4设计源及产物指纹；Git审查头由PR与提交后复核快照固定，不在生成物内追写自身SHA',
        'checks':deliveries,'commands':['python docs/D1B/生成/build_design.py','python docs/D1B/生成/build_design.py --check','python docs/D1B/生成/test_build_design.py'],
        'scope':'MD/HTML及公共证据结构，非产品功能测试；HTML目视记录见审核记录'})
    summary={'pages':len(data['pages']),'controls':len(controls),'interactive':sum(c[2] not in ('STATIC','msctls_progress32') for c in controls),'tab_stops':sum(len(t['control_ids']) for t in tabs),'fields':len(fields),'import_fields':len(data['import_fields']),'editable_fields':len(data['editable_fields']),'templates':len(data['templates']),'static_checks':len(checks),'delivery_checks':len(deliveries),'negative_checks':len(negative),'failed':[r for r in checks+deliveries+negative if not r['pass']]}
    return products,summary

def build(check_only=False):
    products,summary=generate_products()
    # CRLF/LF differences count as drift: compare the exact deterministic bytes.
    if check_only:
        drift=[p.relative_to(ROOT).as_posix() for p,text in products.items() if not p.exists() or p.read_bytes()!=text.encode('utf-8')]
        summary.update({'mode':'check','drift':drift,'writes':0})
    else:
        drift=[]
        if not summary['failed']:
            for p,text in products.items():
                p.parent.mkdir(parents=True,exist_ok=True)
                p.write_bytes(text.encode('utf-8'))
        summary['mode']='build'
    print(json_text(summary))
    if summary['failed'] or drift:
        raise SystemExit(1)
    return summary

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true',help='只读重建比较；任何产物不一致返回1，不写文件')
    build(parser.parse_args().check)
