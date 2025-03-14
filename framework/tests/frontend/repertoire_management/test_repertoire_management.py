import pytest

pytestmark = [pytest.mark.repertoire_management]

@pytest.mark.smoke_tests
@pytest.mark.parametrize(
    'products_supported',
    [('Modules', 'Repertoire Management Module', 'Products Supported', 'There are several types of Product Supported:')],
    indirect=True)
def test_verify_products_supported(products_supported):
    """
    test_verify_products_supported()

    :Scenario: Verify the list of products supported under the "Products Supported" section under
               "Repertoire Management".
    :Given: The user is on the Matching Engine Home page.
    :When: The user clicks on the "Repertoire Management Module" header option.
    :And: The user clicks on the "Products Supported" link under "Additional Features".
    :Then: The user should only see the mentioned list of products supported under the "Products Supported" section.
    """
    products_supported_list = ['Cue Sheet / AV Work', 'Recording', 'Bundle', 'Advertisement']
    products_supported.assert_products_supported(products_supported.config.products_list, products_supported_list)
