from .utils import relative_folder


def build_xslt_dict(configuration_file, configuration_path):
    """

    :param configuration_file:
    :param configuration_path:
    :return:
    """
    xslt_dict = {}

    for xsl in configuration_file.xpath(".//xslts/default/text()"):
        xslt_dict["default"] = relative_folder(configuration_path, xsl)

    for xsl in configuration_file.xpath(".//xslts/xsl"):
        xslt_dict[xsl.get("identifier")] = relative_folder(configuration_path, xsl.text)

    return xslt_dict
