
res = ps.get('products', 411)

del res['product']['id']
del res['product']['position_in_category']
del res['product']['manufacturer_name']
del res['product']['id_default_image']
del res['product']['quantity']


del res['product']['associations']['images']

edit: 
del res['product']['position_in_category']
del res['product']['manufacturer_name']
del res['product']['quantity']

res['product']['name']['language']['value']=
res['product']['description']['language']['value']=

