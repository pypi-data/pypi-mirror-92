import xml.etree.ElementTree as ET

from tavalidate.log import logger


def do_assert_xml(resp, **kwargs):
    """
    Assert the xml structure in response body is the same as the expected xml.

    :param resp:
    :param expected: The expected xml string
    :param strict: The response xml should not have extra attributes or children
    :return:
    """
    expected_xml = kwargs['expected']
    strict = kwargs.get('strict', False)
    source_xml = resp.text
    logger.debug("Response body: {}".format(source_xml))
    source_et = ET.fromstring(source_xml)
    expected_et = ET.fromstring(expected_xml)
    assert source_et is not None, "Can not parse response body"
    assert expected_et is not None, "Can not parse expected body"
    _assert_node(source_et, expected_et, strict)


def _assert_node(source, expected, strict):
    assert source.tag == expected.tag, \
        "Tag {} is different from expected {}".format(source.tag, expected.tag)
    for attr in expected.attrib:
        assert attr in source.attrib, \
            "Attribute {} not found in {}".format(attr, source.tag)
        assert _assert_value(source.attrib[attr], expected.attrib[attr]), \
            "Expecting attribute {}, but get {}".format(expected.attrib[attr],
                                                        source.attrib[attr])
    if strict:
        for attr in source.attrib:
            assert attr in expected.attrib, \
                "Attribute {} in {} is unexpected and we're in strict mode".format(
                        attr, expected.tag)
    assert _assert_value(source.text, expected.text), \
        "Node value {} not equal to expected {} in {}".format(
                source.text, expected.text, expected.tag)
    validated_child_tags = set()
    for child in expected:
        if child.tag not in validated_child_tags:
            validated_child_tags.add(child.tag)
            expected_children = expected.iter(child.tag)
            source_children = source.iter(child.tag)
            expected_list = list(expected_children)
            source_list = list(source_children)
            assert source_children is not None, \
                "Tag {} not found in {}".format(child.tag, expected.tag)
            for idx, expected_child in enumerate(expected_list):
                assert idx < len(source_list), \
                    "Tag {} inside {} should have {} occurrences, " \
                    "but {} is found".format(child.tag, source.tag,
                                             len(expected_list),
                                             len(source_list))
                source_child = source_list[idx]
                _assert_node(source_child, expected_child, strict)
    if strict:
        for child in source:
            expected_child = source.find(child.tag)
            assert expected_child is not None, \
                "Tag {} in {} is unexpected and we're in strict mode.".format(
                        child, expected.tag)


def _assert_value(source: str, expected: str):
    if source is None and expected is None:
        return True
    if expected is None and source is not None and not source.strip():
        return True
    if expected is None:
        return False
    expected_striped = expected.strip()
    if source is None and not expected_striped:
        return True
    if expected_striped == "!anything":
        return True
    elif expected_striped == "!anyint":
        try:
            int(source.strip())
            return True
        except ValueError:
            assert False, "{} is not a integer".format(source)
    elif expected_striped == "!anyfloat":
        try:
            float(source.strip())
            return True
        except ValueError:
            assert False, "{} is not a float".format(source)
    elif expected_striped == "!anystr":
        return True
    elif expected_striped == "!anybool":
        try:
            bool(source.strip())
            return True
        except ValueError:
            assert False, "{} is not a bool".format(source)
    if source is None:
        return False
    return source.strip() == expected_striped


assert_xml = do_assert_xml
