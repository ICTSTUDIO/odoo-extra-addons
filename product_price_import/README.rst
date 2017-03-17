====================
Product Price import
====================


The CSV file must have a header line with the following fields:

Import Cost Price:
- productcode (The default_code of products in ODOO)
- kostprijs (The standard_price in ODOO)

Import Sale Price:
- productcode (The default_code of products in ODOO)
- verkoopprijs (The list_price in ODOO)

Import Purchase Price:
- productcode
- inkoopprijs

Import Pricelist:
- productcode (The product_code of Supplierinfo or default_code of products in ODOO)
- stuks (The min_qty in Pricelist item)
- prijs (The price_surcharge of a pricelist item, with price_discount = -1)
