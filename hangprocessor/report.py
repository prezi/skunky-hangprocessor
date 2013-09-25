import genshi.template, sys, os, json, re
from signatures import getDumpInfo

thisdir = os.path.dirname(__file__)
tmpl = genshi.template.MarkupTemplate(open(os.path.join(thisdir, 'report.xhtml')))

whitelist = set( (
    'Accessibility',
    'AdapterDeviceID',
    'AdapterVendorID',
    'additional_minidumps',
    'Add-ons',
    'BuildID',
    'CpuUsageFlashProcess1',
    'CpuUsageFlashProcess2',
    'CrashTime',
    'EMCheckCompatibility',
    'FramePoisonBase',
    'FramePoisonSize',
    'InstallTime',
    'Notes',
    'NumberOfProcessors',
    'PluginCpuUsage',
    'PluginFilename',
    'PluginHang',
    'ProcessType',
    'ProductID',
    'ProductName',
    'ReleaseChannel',
    'StartupTime',
    'submitted_timestamp',
    'Theme',
    'Throttleable',
    'Vendor',
    'Version',
    'Winsock_LSP',

    'prezi_oid',
    'Android_Manufacturer',
    'Android_Model',
    'Android_Board',
    'Android_Brand',
    'Android_Device',
    'Android_Display',
    'Android_Fingerprint',
    'Android_CPU_ABI',
    'Android_CPU_ABI2',
    'Android_Hardware',
    'Android_Version'
) )

okchars = re.compile('[a-zA-Z0-9]+$')

def generateReport(reportdir):
    if reportdir[-1] == os.sep:
        reportdir = reportdir[:-1]

    uuid = os.path.basename(reportdir)

    extra = json.load(open(os.path.join(reportdir, 'extra.json')))

    dumps = {}

    def loaddump(name):
        basepath = os.path.join(reportdir, 'minidump_%s.dmp' % name)
        
        dumps[name] = getDumpInfo(basepath)

    loaddump('plugin')
    for d in extra.get(u'additional_minidumps', '').split(','):
        if not okchars.match(d):
            continue

        loaddump(d)

    s = tmpl.generate(id=uuid, extra=extra, dumps=dumps, whitelist=whitelist)
    return s.render('html')

if __name__ == '__main__':
    reportdir, = sys.argv[1:]
    print generateReport(reportdir)
