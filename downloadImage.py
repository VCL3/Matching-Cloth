from gilt.rest import GiltApiClient
from defClothes import *
import urllib



# Create client using api_key
client = GiltApiClient(api_key = '4bc9ea982749056525a630ff9eb6deda9f737c2a94492963f29e32f077ed766f')

# Get Active Sales info, go to men store, need to check what sales there are
# print 'Number of sales: ', len(client.sales.active('men'))

# usefulsale = [3, 5, 6, 7, 8, 9, 10, 11, 18, 22, 23, 24, 25, 26]
i = 0
startIndex = 722

outfile = open("inputs/gilt.dat", "w")

for sale in client.sales.active('men'):
  product_urls = sale.products
  if not product_urls: continue

  # print 'First %d products (of %d) of sale "%s"' % (len(product_urls), len(sale.products), sale.name)
    
  for url in product_urls:
    try:
      product = client.products.get(url=url) 
      name = product.name.split()
      category = name[len(name)-1].lower()
      for item in article_list:
        if category in item:
          startIndex += 1
          print category 
          outfile.write(str(startIndex) + " " + category)
          outfile.write("\n")
          for image in product.image_urls.image_list("300x400"):
            # print image.url
            urllib.urlretrieve(image.url, "img/lg-" + str(startIndex) + ".jpg")
            break
    except:
      continue

    # print '  %s:' % product.name
    # print '    Web:    %s' % product.url
    # print '    Brand:  %s' % product.brand
    # print '    Origin: %s' % product.content.origin
    # print '    Images in %d resolution(s): %s'  % (
    #   len(product.image_urls), 
    #   ', '.join(["%s x %s" % (w,h) for (w,h) in product.image_urls.image_sizes])
    #   )
    # for sku in product.skus:
    #   if 'color' in sku.attribute_names() and 'size' in sku.attribute_names():
    #     desc = 'Sku %s is %s size %s' % (sku.id, sku.attribute('color').value, sku.attribute('size').value)
    #   else:
    #     desc = 'Sku %s: %s' % (sku.id, ', '.join("%s=%s" % (k, sku.attribute(k).value) for k in sku.attribute_names()))
    #   print '      %-45s   Gilt: $%1.2f   MSRP $%1.2f' % (desc, sku.sale_price, sku.msrp_price)
      
outfile.close()

