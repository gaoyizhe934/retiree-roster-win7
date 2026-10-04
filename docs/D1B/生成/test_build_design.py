"""故意损坏输入验证生成器确实拒绝CV4/UI回退；非产品运行测试。"""
import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import contextmanager
from unittest import mock
sys.dont_write_bytecode = True

def negative_results(builder):
    header=(builder.ROOT/'include/retiree_roster/schema_types.hpp').read_text(encoding='utf-8')
    data=json.loads((builder.HERE/'设计数据.json').read_text(encoding='utf-8'))
    assembled=builder.assemble_data(header,data)
    data=assembled['data']; layouts=assembled['layouts']
    md=builder.render_source_markdown((builder.HERE/'设计正文.md').read_text(encoding='utf-8'),data)
    def evaluate(h,m,d):
        return {x['check']:x['pass'] for x in builder.static_checks(h,m,d,d['fields'],d['tabs'],layouts)}
    baseline=evaluate(header,md,data)
    results=[builder.check_row('反例前完整输入通过',all(baseline.values()),'先验证所有静态检查通过，避免因原输入失败产生假阳性')]
    scenarios=[
        ('ImportFieldId显式映射完整',lambda h,m,d:(h.replace('case ImportFieldId::EmployeeNo: *out = FieldId::EmployeeNo;', 'case ImportFieldId::EmployeeNo: *out = FieldId::FullName;'),m,d)),
        ('EditableFieldId显式映射完整',lambda h,m,d:(h.replace('case EditableFieldId::FullName: *out = FieldId::FullName;', 'case EditableFieldId::FullName: *out = FieldId::Remark;'),m,d)),
        ('CV4版本与基线身份',lambda h,m,d:(h.replace('kCurrentContractVersion = 4U','kCurrentContractVersion = 3U'),m,d)),
        ('FieldChange日期payload',lambda h,m,d:(h.replace('return change.value.empty() && change.date_value.is_known();','return true;'),m,d)),
        ('FieldChange文本枚举payload',lambda h,m,d:(h.replace('return empty_date;','return true;'),m,d)),
        ('clear规范Unknown',lambda h,m,d:(h.replace('if (change.clear_value) { return change.value.empty() && empty_date; }','if (change.clear_value) { return true; }'),m,d)),
        ('RosterResult没有可写人数',lambda h,m,d:(h.replace('std::size_t total_count() const { return rows.size(); }','std::size_t total_count = 0;'),m,d)),
        ('YearCount空启用拒绝',lambda h,m,d:(h.replace('condition.accepted_values.empty() && !condition.has_minimum','false'),m,d)),
        ('YearCount负值拒绝',lambda h,m,d:(h.replace('condition.minimum < 0','false'),m,d)),
        ('Confirm源身份与checked copy',lambda h,m,d:(h,m.replace('可重读源字节验证 SHA/identity','确认不重读原文件'),d)),
    ]
    scenarios.extend([
        ('SP1目标名称',lambda h,m,d:(h,m.replace('Windows 7 SP1','Win7 RTM'),d)),
        ('SP1系统版本',lambda h,m,d:(h,m.replace('6.1.7601','6.1.7600'),d)),
        ('Q项无第二业务工作簿未决',lambda h,m,d:(h,m+'\n| Q02 | 第二份样表待确认 | A | 待确认 |\n',d)),
        ('Q项无两区域性质未决',lambda h,m,d:(h,m+'\n| Q05 | 行1/行3性质待确认 | A | 待确认 |\n',d)),
    ])
    for name,mutate in scenarios:
        h,m,d=mutate(header,md,copy.deepcopy(data))
        result=evaluate(h,m,d)
        results.append(builder.check_row('反例：'+name,baseline.get(name) is True and result.get(name) is False,'故意回退输入；对应检查应失败'))
    # Change the expected fingerprint, without touching controlled documents.
    rel='docs/退休人员名册打印小程序需求说明.docx'
    name='原始资料指纹：退休人员名册打印小程序需求说明.docx'
    current_sha=builder.BASELINES[rel]
    try:
        builder.BASELINES[rel]='658b10952e2cba734990d2b37f862b2495196e51427c117cf2a4edde7992c641'
        result=evaluate(header,md,data)
        results.append(builder.check_row('反例：v2.1指纹回退v2.0',baseline.get(name) is True and result.get(name) is False,'旧SHA必须被当前受控文件检查拒绝'))
    finally:
        builder.BASELINES[rel]=current_sha
    mutations=[
        ('SourceProfile范围与冻结区分',lambda d:d['source_profile_scope'].update(import_profile_status='已冻结')),
        ('FullName禁止UI清空',lambda d:next(f for f in d['fields'] if f['id']=='FullName')['ui_override'].update(ordinary_clear_allowed=True)),
        ('既有状态日期单入口',lambda d:next(f for f in d['fields'] if f['id']=='DeathDate')['ui_override'].update(existing_readonly=False)),
        ('筛选白名单排除系统敏感',lambda d:d['filterable_fields'].append('NationalId')),
        ('按类型限定Comparison',lambda d:d['filter_comparisons']['EnumCode'].append('Contains')),
        ('Unknown日期UI空白',lambda d:next(c for c in d['controls'] if c[3]=='DateValue.year').__setitem__(4,'0／原值')),
        ('未闭环报告默认禁用',lambda d:next(c for c in d['controls'] if c[0]=='P14-04').__setitem__(4,'可用')),
        ('搜索语义候选待确认',lambda d:next(c for c in d['controls'] if c[0]=='P20-01').__setitem__(3,'姓名精确查询')),
        ('初始焦点属于本页控件',lambda d:next(t for t in d['tabs'] if t['page']=='P22').update(initial_focus='missing-control')),
        ('语义锚点完整输出',lambda d:d['semantic_anchors'].update(confirm_source_identity='')),
    ]
    for name,mutate in mutations:
        broken=copy.deepcopy(data);mutate(broken)
        result=evaluate(header,md,broken)
        results.append(builder.check_row('反例：'+name,baseline.get(name) is True and result.get(name) is False,'故意错误UI数据；对应检查应失败'))
    html_doc=builder.make_html(md,data['flow_model'])
    def delivered(text, html_text):
        return {r['check']:r['pass'] for r in builder.delivery_checks(text,html_text,data,text+html_text)}
    valid=delivered(md,html_doc)
    for href in ('javascript:alert%281%29','data:text/html,evil','//outside/share/x','C:/outside/x','../../../outside/x'):
        damaged=md+'\n[无效链接]('+href+')\n'
        html_broken=html_doc+'<a href="'+href+'">无效链接</a>'
        result=delivered(damaged,html_broken)
        results.append(builder.check_row('反例：危险链接 '+href.split(':')[0],
            valid['文档本地链接有效'] and valid['HTML链接协议与仓库边界']
            and not result['文档本地链接有效'] and not result['HTML链接协议与仓库边界'],
            'Markdown与实际a[href]都必须显式拒绝'))
    broken_flow=md.replace('P10[选择文件]','P10[故意改名]')
    result=delivered(broken_flow,html_doc)
    results.append(builder.check_row('反例：Mermaid节点漂移',valid['SVG与Mermaid节点一致']
        and not result['SVG与Mermaid节点一致'],'保持SVG模型不变，只改Mermaid标签'))
    broken_edges=md.replace('P01 --> P10','P01 --> P11')
    result=delivered(broken_edges,html_doc)
    results.append(builder.check_row('反例：Mermaid路径漂移',valid['SVG与Mermaid路径一致']
        and not result['SVG与Mermaid路径一致'],'核心边变更必须使交付检查失败'))
    return results

@contextmanager
def repository_fixture(builder):
    """The production input declaration owns the external fixture files."""
    with tempfile.TemporaryDirectory(prefix='d1b-check-') as tmp:
        root=Path(tmp)
        shutil.copytree(builder.OUT,root/'docs/D1B',ignore=shutil.ignore_patterns('__pycache__'))
        for rel in builder.ROOT_INPUT_FILES:
            target=root/rel; target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(builder.ROOT/rel,target)
        yield root, root/'docs/D1B/生成/build_design.py'

def tree_bytes(root):
    return {p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file()}

def run_builder(script, *args, cp936=False):
    env=os.environ.copy()
    if cp936:
        env['PYTHONIOENCODING']='cp936'
        env['PYTHONUTF8']='0'
    return subprocess.run([sys.executable,str(script),*args],capture_output=True,env=env)

class GeneratorRegression(unittest.TestCase):
    def test_contract_and_ui_negative_controls(self):
        import build_design
        results=negative_results(build_design)
        self.assertEqual([], [r for r in results if not r['pass']])

    def test_check_detects_drift_without_writing(self):
        import build_design
        products,summary=build_design.generate_products()
        self.assertFalse(summary['failed'])
        # Build a minimal temporary repository fixture; do not damage the delivery.
        with repository_fixture(build_design) as (root,script):
            proc=run_builder(script)
            self.assertEqual(0,proc.returncode,proc.stdout.decode('utf-8',errors='replace'))
            proc=run_builder(script,'--check')
            self.assertEqual(0,proc.returncode,proc.stdout.decode('utf-8',errors='replace'))
            target=root/'docs/D1B/D1B_使用流程与模板设计.html'
            target.write_bytes(target.read_bytes()+b'\nDRIFT\n')
            before=tree_bytes(root)
            proc=run_builder(script,'--check')
            self.assertEqual(1,proc.returncode)
            report=json.loads(proc.stdout.decode('utf-8'))
            self.assertIn('docs/D1B/D1B_使用流程与模板设计.html',report['drift'])
            after=tree_bytes(root)
            self.assertEqual(before,after,'--check不得修改输入或任何产物')

    def test_machine_output_is_utf8_under_cp936(self):
        import build_design
        with repository_fixture(build_design) as (root,script):
            proc=run_builder(script,cp936=True)
            self.assertEqual(0,proc.returncode,proc.stderr)
            self.assertEqual([],json.loads(proc.stdout.decode('utf-8'))['failed'])
            before=tree_bytes(root)
            proc=run_builder(script,'--check',cp936=True)
            self.assertEqual(0,proc.returncode,proc.stderr)
            self.assertEqual([],json.loads(proc.stdout.decode('utf-8'))['drift'])
            self.assertEqual(before,tree_bytes(root))
            target=root/'docs/D1B/D1B_使用流程与模板设计.html'
            target.write_bytes(target.read_bytes()+b'\nDRIFT\n')
            before=tree_bytes(root)
            proc=run_builder(script,'--check',cp936=True)
            self.assertEqual(1,proc.returncode,proc.stderr)
            report=json.loads(proc.stdout.decode('utf-8'))
            self.assertIn('docs/D1B/D1B_使用流程与模板设计.html',report['drift'])
            self.assertEqual(0,report['writes'])
            self.assertEqual(before,tree_bytes(root))

    def test_missing_baseline_is_structured_utf8_failure(self):
        import build_design
        with repository_fixture(build_design) as (root,script):
            (root/next(iter(build_design.BASELINES))).unlink()
            before=tree_bytes(root)
            for args in ((),('--check',)):
                proc=run_builder(script,*args,cp936=True)
                self.assertEqual(1,proc.returncode)
                report=json.loads(proc.stdout.decode('utf-8'))
                self.assertTrue(any('文件缺失' in r['detail'] for r in report['failed']))
                self.assertNotIn(b'Traceback',proc.stderr)
                self.assertEqual(before,tree_bytes(root))

    def test_dangerous_links_never_probe_outside_repository(self):
        import build_design
        bad=('javascript:alert%281%29','data:text/html,evil','file:///outside',
             'ftp://outside','http://outside','//host/share','\\\\host\\share',
             'C:/outside','C:\\outside','/outside','../../../outside',
             '%2F%2Fhost/share','%2e%2e/%2e%2e/%2e%2e/outside')
        with mock.patch.object(Path,'exists',side_effect=AssertionError('禁止外部探测')) as exists:
            for href in bad:
                with self.subTest(href=href):
                    self.assertFalse(build_design.href_is_valid(href))
                    self.assertNotIn('<a ',build_design.inline('[禁止]('+href+')'))
            exists.assert_not_called()
        self.assertEqual('https',build_design.classify_href('https://github.com/example')[0])
        self.assertEqual('anchor',build_design.classify_href('#section-1')[0])
        self.assertTrue(build_design.href_is_valid('README.md'))

    def test_struct_members_accept_simple_initializer_styles(self):
        import build_design
        for declaration in ('std::size_t x;','std::size_t x = 0;',
                            'std::size_t x{0};','std::size_t x{};'):
            with self.subTest(declaration=declaration):
                self.assertEqual(['x'],build_design.struct_members('struct Example { '+declaration+' };','Example'))
        self.assertEqual(['rows'],build_design.struct_members(
            'struct Example { std::vector<int> rows; std::size_t count() const { return rows.size(); } };','Example'))

    def test_assembly_preserves_source_and_create_only_tabs(self):
        import build_design
        source=json.loads((build_design.HERE/'设计数据.json').read_text(encoding='utf-8'))
        before=copy.deepcopy(source)
        header=(build_design.ROOT/build_design.ROOT_INPUT_FILES[0]).read_text(encoding='utf-8')
        assembled=build_design.assemble_data(header,source)
        self.assertEqual(before,source)
        row=next(t for t in assembled['tabs'] if t['page']=='P22')
        self.assertTrue(row['create_only_control_ids'])
        self.assertEqual('P22-F04',row['initial_focus'])

    def test_semantic_anchor_updates_are_single_source(self):
        import build_design
        source=(build_design.HERE/'设计正文.md').read_text(encoding='utf-8')
        data=json.loads((build_design.HERE/'设计数据.json').read_text(encoding='utf-8'))
        key='confirm_source_identity'
        self.assertIn('{{semantic.'+key+'}}',source)
        self.assertNotIn(data['semantic_anchors'][key],source)
        data['semantic_anchors'][key]='源字节再次读取只用于核对SHA与identity'
        rendered=build_design.render_semantic_anchors(source,data)
        self.assertIn(data['semantic_anchors'][key],rendered)
        header=(build_design.ROOT/build_design.ROOT_INPUT_FILES[0]).read_text(encoding='utf-8')
        assembled=build_design.assemble_data(header,data)
        checks=build_design.static_checks(header,rendered,assembled['data'],assembled['fields'],assembled['tabs'],assembled['layouts'])
        self.assertTrue(next(r['pass'] for r in checks if r['check']=='Confirm源身份与checked copy'))

if __name__=='__main__':
    unittest.main(verbosity=2)
