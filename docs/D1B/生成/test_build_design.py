"""故意损坏输入验证生成器确实拒绝CV4/UI回退；非产品运行测试。"""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
sys.dont_write_bytecode = True

def negative_results(builder):
    header=(builder.ROOT/'include/retiree_roster/schema_types.hpp').read_text(encoding='utf-8')
    data=json.loads((builder.HERE/'设计数据.json').read_text(encoding='utf-8'))
    fields=builder.load_contract(header)
    controls,field_rows=builder.make_controls(data,fields)
    data.update({'contract_version':4,'fields':field_rows,'controls':controls,
        'import_fields':[x for x in builder.enum_members(header,'ImportFieldId') if x!='Unspecified'],
        'editable_fields':[x for x in builder.enum_members(header,'EditableFieldId') if x!='Unspecified']})
    tabs=[]
    for pid,page in data['pages'].items():
        interactive=[r for r in page['controls'] if r[2] not in ('STATIC','msctls_progress32') and r[0] not in builder.PENDING_INTERFACE_CONTROLS]
        tabs.append({'control_ids':[r[0] for r in interactive],'create_only_control_ids':[]})
    md=(builder.HERE/'设计正文.md').read_text(encoding='utf-8')
    _,layouts=builder.template_sections(data['templates'])
    def evaluate(h,m,d):
        return {x['check']:x['pass'] for x in builder.static_checks(h,m,d,d['fields'],tabs,layouts)}
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
    for name,mutate in scenarios:
        h,m,d=mutate(header,md,copy.deepcopy(data))
        result=evaluate(h,m,d)
        results.append(builder.check_row('反例：'+name,baseline.get(name) is True and result.get(name) is False,'故意回退输入；对应检查应失败'))
    mutations=[
        ('FullName禁止UI清空',lambda d:next(f for f in d['fields'] if f['id']=='FullName')['ui_override'].update(ordinary_clear_allowed=True)),
        ('既有状态日期单入口',lambda d:next(f for f in d['fields'] if f['id']=='DeathDate')['ui_override'].update(existing_readonly=False)),
        ('筛选白名单排除系统敏感',lambda d:d['filterable_fields'].append('NationalId')),
        ('按类型限定Comparison',lambda d:d['filter_comparisons']['EnumCode'].append('Contains')),
        ('Unknown日期UI空白',lambda d:next(c for c in d['controls'] if c[3]=='DateValue.year').__setitem__(4,'0／原值')),
        ('未闭环报告默认禁用',lambda d:next(c for c in d['controls'] if c[0]=='P14-04').__setitem__(4,'可用')),
        ('搜索语义候选待确认',lambda d:next(c for c in d['controls'] if c[0]=='P20-01').__setitem__(3,'姓名精确查询')),
    ]
    for name,mutate in mutations:
        broken=copy.deepcopy(data);mutate(broken)
        result=evaluate(header,md,broken)
        results.append(builder.check_row('反例：'+name,baseline.get(name) is True and result.get(name) is False,'故意错误UI数据；对应检查应失败'))
    return results

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
        with tempfile.TemporaryDirectory(prefix='d1b-check-') as tmp:
            root=Path(tmp)
            import shutil
            shutil.copytree(build_design.OUT,root/'docs/D1B',ignore=shutil.ignore_patterns('__pycache__'))
            for rel in list(build_design.BASELINES)+['include/retiree_roster/schema_types.hpp']:
                target=root/rel;target.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(build_design.ROOT/rel,target)
            script=root/'docs/D1B/生成/build_design.py'
            proc=subprocess.run([sys.executable,str(script)],capture_output=True)
            self.assertEqual(0,proc.returncode,proc.stdout.decode('utf-8',errors='replace'))
            proc=subprocess.run([sys.executable,str(script),'--check'],capture_output=True)
            self.assertEqual(0,proc.returncode,proc.stdout.decode('utf-8',errors='replace'))
            target=root/'docs/D1B/D1B_使用流程与模板设计.html'
            target.write_bytes(target.read_bytes()+b'\nDRIFT\n')
            before={p.relative_to(root).as_posix():p.read_bytes() for p in (root/'docs/D1B').rglob('*') if p.is_file()}
            proc=subprocess.run([sys.executable,str(script),'--check'],capture_output=True)
            self.assertEqual(1,proc.returncode)
            report=json.loads(proc.stdout.decode('utf-8'))
            self.assertIn('docs/D1B/D1B_使用流程与模板设计.html',report['drift'])
            after={p.relative_to(root).as_posix():p.read_bytes() for p in (root/'docs/D1B').rglob('*') if p.is_file()}
            self.assertEqual(before,after,'--check不得修改输入或任何产物')

if __name__=='__main__':
    unittest.main(verbosity=2)
