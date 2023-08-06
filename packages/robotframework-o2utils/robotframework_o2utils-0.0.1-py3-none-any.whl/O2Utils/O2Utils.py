from robot.api.deco import keyword


class O2Utils:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '1.0.0'

    @keyword('Change XML Parameters')
    def change_xml_parameters(self, xmlstring, param_dictionary):
        """ Replace parameters in string XML with dictionary as argument """
        for key in param_dictionary:
            xmlstring = xmlstring.replace("{" + key + "}", param_dictionary[key])
        return xmlstring
