from PySide2 import QtWidgets

from famegui.ui_newagent_dialog import Ui_NewAgentDialog

from famegui import models


class NewAgentDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self._ui = Ui_NewAgentDialog()
        self._ui.setupUi(self)
        # init
        self.setWindowTitle("New agent")
        self._ui.comboBoxType.addItems(self._agent_type_list())
        # tree view
        self._ui.treeFields.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self._ui.treeFields.setRootIsDecorated(False)
        self._ui.treeFields.setColumnCount(2)
        self._ui.treeFields.setHeaderLabels(["Field", "Value"])
        self._ui.treeFields.setColumnWidth(0, 200)
        self._ui.treeFields.setAlternatingRowColors(True)
        self._fill_input_fields_table()
        # connect slots
        self._ui.comboBoxType.currentTextChanged.connect(
            self._fill_input_fields_table)

    def _fill_input_fields_table(self):
        self._ui.treeFields.clear()
        fields = self._field_list_for_agent_type(
            self._ui.comboBoxType.currentText())
        for f in fields:
            QtWidgets.QTreeWidgetItem(self._ui.treeFields, [f, ""])

    def make_new_agent(self, agent_id) -> models.Agent:
        agent_type = self._ui.comboBoxType.currentText()
        return models.Agent(agent_id, agent_type)

    def _agent_type_list(self):
        return self._inputs_by_agent_type.keys()

    def _field_list_for_agent_type(self, agent_type: str):
        return self._inputs_by_agent_type[agent_type].keys()

    _inputs_by_agent_type = {
        "EnergyExchange": {
            "DistributionMethod": {
                "FieldType": "enum",
                "Mandatory": True,
                "Values": ['SAME_SHARES']
            }
        },
        "SystemOperatorTrader": {
        },
        "CarbonMarket": {
            "Co2Prices": {
                "FieldType": "time_series",
                "Mandatory": True,
            },
            "OperationMode": {
                "FieldType": "enum",
                "Mandatory": True,
                "Values": ['FIXED'],
            },
        },
        "FuelsMarket": {
            "NATURAL_GAS": {
                "FieldType": "time_series",
                "Mandatory": False,
            },
            "NUCLEAR": {
                "FieldType": "time_series",
                "Mandatory": False,
            },
            "LIGNITE": {
                "FieldType": "time_series",
                "Mandatory": False,
            },
            "HARD_COAL": {
                "FieldType": "time_series",
                "Mandatory": False,
            },
            "OIL": {
                "FieldType": "time_series",
                "Mandatory": False,
            },
            "WASTE": {
                "FieldType": "time_series",
                "Mandatory": False,
            },
            "OIL_CF": {
                "FieldType": "double",
                "Mandatory": False,
            },
            "HARD_COAL_CF": {
                "FieldType": "double",
                "Mandatory": False,
            },
            "LIGNITE_CF": {
                "FieldType": "double",
                "Mandatory": False,
            },
            "NUCLEAR_CF": {
                "FieldType": "double",
                "Mandatory": False,
            },
            "WASTE_CF": {
                "FieldType": "double",
                "Mandatory": False,
            },
            "NATURAL_GAS_CF": {
                "FieldType": "double",
                "Mandatory": False,
            },
        },
        "DemandTrader": {
            "DemandSeries": {
                "FieldType": "time_series",
                "Mandatory": True,
            },
            "ValueOfLostLoad": {
                "FieldType": "double",
                "Mandatory": True,
            },
        },
        "PriceForecaster": {
            "DistributionMethod": {
                "FieldType": "enum",
                "Mandatory": True,
                "Values": ['SAME_SHARES'],
            },
            "ForecastPeriodInHours": {
                "FieldType": "integer",
                "Mandatory": True,
            },
            "ForecastRequestOffsetInSeconds": {
                "FieldType": "integer",
                "Mandatory": True,
            },
        },
        "StorageTrader": {
            "DispatchSchedule": {
                "FieldType": "time_series",
                "Mandatory": False,
            },
            "ForecastPeriodInHours": {
                "FieldType": "integer",
                "Mandatory": True,
            },
            "ForecastRequestOffsetInSeconds": {
                "FieldType": "integer",
                "Mandatory": True,
            },
            "PriceForecastErrorInEURPerMWH": {
                "FieldType": "double",
                "Mandatory": True,
            },
            "PowerInMW": {
                "FieldType": "double",
                "Mandatory": True,
            },
            "EnergyToPowerRatio": {
                "FieldType": "double",
                "Mandatory": True,
            },
            "ChargeEfficiency": {
                "FieldType": "double",
                "Mandatory": True,
            },
            "DischargeEfficiency": {
                "FieldType": "double",
                "Mandatory": True,
            },
            "SelfDischargeRatePerHour": {
                "FieldType": "double",
                "Mandatory": True,
            },
            "InitialEnergyLevelInMWH": {
                "FieldType": "double",
                "Mandatory": True,
            },
            "ScheduleDurationInHours": {
                "FieldType": "integer",
                "Mandatory": True,
            },
            "StrategistType": {
                "FieldType": "enum",
                "Mandatory": True,
                "Values": ['SINGLE_AGENT_MAX_PROFIT', 'SINGLE_AGENT_MIN_SYSTEM_COST', 'MULTI_AGENT_SIMPLE', 'DISPATCH_FILE'],
            },
            "PurchaseLeviesAndTaxesInEURperMWH": {
                "FieldType": "double",
                "Mandatory": True,
            },
            "ModelledChargingSteps": {
                "FieldType": "integer",
                "Mandatory": True,
            },
            "AssessmentFunctionPrefactors": {
                "FieldType": "double_list",
                "Mandatory": False,
            },
        },
        "ConventionalPlantOperator": {
        },
        "PredefinedPlantBuilder": {
            "InstalledPowerInMW": {
                "FieldType": "time_series",
                "Mandatory": True,
            },
            "OpexVarInEURperMWH": {
                "FieldType": "time_series",
                "Mandatory": True,
            },
            "PlannedAvailability": {
                "FieldType": "time_series",
                "Mandatory": True,
            },
            "MaxEfficiency": {
                "FieldType": "time_series",
                "Mandatory": True,
            },
            "MinEfficiency": {
                "FieldType": "time_series",
                "Mandatory": True,
            },
            "BlockSizeInMW": {
                "FieldType": "double",
                "Mandatory": True,
            },
            "CyclingCostInEURperMW": {
                "FieldType": "double",
                "Mandatory": True,
            },
            "SpecificCo2EmissionsInTperMWH": {
                "FieldType": "double",
                "Mandatory": True,
            },
            "UnplannedAvailabilityFactor": {
                "FieldType": "double",
                "Mandatory": True,
            },
            "FuelType": {
                "FieldType": "enum",
                "Mandatory": True,
                "Values": ['LIGNITE', 'OIL', 'WASTE', 'NUCLEAR', 'HARD_COAL', 'NATURAL_GAS'],
            },
        },
        "ConventionalTrader": {
            "minMarkup": {
                "FieldType": "double",
                "Mandatory": True,
            },
            "maxMarkup": {
                "FieldType": "double",
                "Mandatory": True,
            },
        },
        "Photovoltaic": {
            "InstalledPowerInMW": {
                "FieldType": "time_series",
                "Mandatory": True,
            },
            "OpexVarInEURperMWH": {
                "FieldType": "time_series",
                "Mandatory": True,
            },
            "YieldProfile": {
                "FieldType": "time_series",
                "Mandatory": True,
            },
            "PowerClass": {
                "FieldType": "integer",
                "Mandatory": True,
            },
        },
        "WindOn": {
            "InstalledPowerInMW": {
                "FieldType": "time_series",
                "Mandatory": True,
            },
            "OpexVarInEURperMWH": {
                "FieldType": "time_series",
                "Mandatory": True,
            },
            "YieldProfile": {
                "FieldType": "time_series",
                "Mandatory": True,
            },
            "PowerClass": {
                "FieldType": "integer",
                "Mandatory": True,
            },
        },
        "WindOff": {
            "InstalledPowerInMW": {
                "FieldType": "time_series",
                "Mandatory": True,
            },
            "OpexVarInEURperMWH": {
                "FieldType": "time_series",
                "Mandatory": True,
            },
            "YieldProfile": {
                "FieldType": "time_series",
                "Mandatory": True,
            },
            "PowerClass": {
                "FieldType": "integer",
                "Mandatory": True,
            },
        },
        "RunOfRiver": {
            "InstalledPowerInMW": {
                "FieldType": "time_series",
                "Mandatory": True,
            },
            "OpexVarInEURperMWH": {
                "FieldType": "time_series",
                "Mandatory": True,
            },
            "YieldProfile": {
                "FieldType": "time_series",
                "Mandatory": True,
            },
            "PowerClass": {
                "FieldType": "integer",
                "Mandatory": True,
            },
        },
        "Biogas": {
            "InstalledPowerInMW": {
                "FieldType": "time_series",
                "Mandatory": True,
            },
            "OpexVarInEURperMWH": {
                "FieldType": "time_series",
                "Mandatory": True,
            },
            "FullLoadHoursPerYear": {
                "FieldType": "double",
                "Mandatory": True,
            },
            "OperationMode": {
                "FieldType": "enum",
                "Mandatory": True,
                "Values": ['CONTINUOUS', 'DAY_NIGHT, FLEX_PREMIUM'],
            },
            "PowerClass": {
                "FieldType": "integer",
                "Mandatory": True,
            },
        },
    }
