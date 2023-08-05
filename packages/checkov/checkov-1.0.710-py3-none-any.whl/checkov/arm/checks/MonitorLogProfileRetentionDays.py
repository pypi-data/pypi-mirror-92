from checkov.common.models.enums import CheckResult, CheckCategories
from checkov.arm.base_resource_check import BaseResourceCheck
from checkov.common.util.type_forcers import force_int

# https://docs.microsoft.com/en-us/azure/templates/microsoft.insights/2016-03-01/logprofiles

class MonitorLogProfileRetentionDays(BaseResourceCheck):
    def __init__(self):
        name = "Ensure that Activity Log Retention is set 365 days or greater"
        id = "CKV_AZURE_37"
        supported_resources = ['microsoft.insights/logprofiles']
        categories = [CheckCategories.LOGGING]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf):
        if "properties" in conf:
            if "retentionPolicy" in conf["properties"]:
                if "enabled" in conf["properties"]["retentionPolicy"]:
                    if str(conf["properties"]["retentionPolicy"]["enabled"]).lower() == "true":
                        if "days" in conf["properties"]["retentionPolicy"]:
                            if force_int(conf["properties"]["retentionPolicy"]["days"]) >= 365 or \
                                    force_int(conf["properties"]["retentionPolicy"]["days"]) == 0:
                                return CheckResult.PASSED
        return CheckResult.FAILED

check = MonitorLogProfileRetentionDays()
