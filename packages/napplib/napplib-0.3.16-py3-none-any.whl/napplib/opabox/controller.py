import requests, json, datetime, logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(threadName)-11s %(levelname)-10s %(message)s")

class OpaBoxController:
    @classmethod
    def make_new_product(self, store_product='', parent='', product='', categ_id='', categ=''):
        # verifica se existe relação pai x filho e cria o payload
        if parent:
            payload = {
                "active": False,  #owner chose active or inactive
                "external_id": str(parent["id"]),
                "name": str(parent["name"]),
                "description": str(parent["description"]), #Optional
                "order": 0, # em casos de variantes de produto seguir uma ordem.
                "updated_at": int(datetime.datetime.now().timestamp()),
                "photos": None,
                "presentations": [],
                "product_views": []
            }

            presentations = {}

            product_sequence = 0

            # coleta os atributos do produto filho
            if product.get('attributes'):
                product_sequence += 1
            
                product_view = {
                    "active": True,
                    "id": str(store_product["id"]),
                    "name": str(store_product["productName"]["String"]),
                    "order": 0,
                    "photos": None,
                    "price": store_product["salePrice"],
                    "price_cost": store_product["listPrice"],
                    "stock_quantity": store_product["stockQuantity"],
                    "unit_label": store_product["measurementUnit"]["String"] if store_product["measurementUnit"]["String"] else "UN",
                    "unit_quantity": 1,
                    "view": [],
                }

                if store_product['eanProduct']['String']:
                    product_view.update({
                        "ean": str(store_product['eanProduct']['String'])
                    })
                    product_view.update({
                        "sku": str(store_product['productCode']['String'])
                    })
                else:
                    # product_view.update({
                    #     "ean": str(product['productCode']['String'])
                    # })
                    product_view.update({
                        "sku": str(store_product['productCode']['String'])
                    })

                for attribute in product['attributes']:
                    if attribute['name'].lower() == "cor":
                        if not "cor" in presentations:
                            presentations['cor'] = {
                                "id": str(attribute['id']),
                                "name": "Cor",
                                "options": []
                            }
                        if not str(attribute['values'][0]['id']) in [c['id'] for c in presentations['cor']['options']]:
                            option = {
                                "id": str(attribute['values'][0]['id']),
                                "label": attribute['values'][0]['value']
                            }
                            presentations['cor']['options'].append(option)
                            product_view['view'].append({"option_id": option['id'], 'presentation_id': presentations['cor']['id']})
                        else:
                            option = {}

                            for op in presentations['cor']['options']:
                                if str(attribute['values'][0]['id']) == str(op['id']):
                                    option = op

                            product_view['view'].append({"option_id": option['id'], 'presentation_id': presentations['cor']['id']})

                    if attribute['name'].lower() == 'tamanho':
                        size = attribute['values'][0]['value']
                        if not "tamanho" in presentations:
                            presentations['tamanho'] = {
                                "id": str(attribute['id']),
                                "name": "tamanho",
                                "options": []
                            }

                        if not str(attribute['values'][0]['id']) in [c['id'] for c in presentations['tamanho']['options']]:
                            option = {
                                "id": str(attribute['values'][0]['id']),
                                "label": str(attribute['values'][0]['value'])
                            }
                            presentations['tamanho']['options'].append(option)
                            product_view['view'].append({"option_id": str(option['id']), 'presentation_id': str(presentations['tamanho']['id'])})
                        else:
                            option = {}

                            for op in presentations['tamanho']['options']:
                                if str(attribute['values'][0]['id']) == op['id']:
                                    option = op
                            product_view['view'].append({"option_id": str(option['id']), 'presentation_id': str(presentations['tamanho']['id'])})

                payload['product_views'].append(product_view)

            for key, presentation in presentations.items():
                payload['presentations'].append(presentation)
                
            if product['categories']:
                payload.update({
                    "category_id": str(product['categories'][0]['id']),
                    "category_label": str(product['categories'][0]['name'])
                })

        # caso não haja relação de pai e filho
        if product and not parent:
            payload = {
                "active": False,  #owner chose active or inactive
                "external_id": str(store_product['id']),
                "name": str(store_product["productName"]["String"]),
                "description": str(store_product["productDescription"]["String"]), #Optional
                "order": 0, # em casos de variantes de produto seguir uma ordem.
                "updated_at": int(datetime.datetime.now().timestamp()),
                "photos": None,
                "presentations": [],
                "product_views": []
            }

            if product.get('attributes'):
            
                product_view = {
                    "active": True,
                    "id": str(store_product["id"]),
                    "name": str(store_product["productName"]["String"]),
                    "order": 0,
                    "photos": None,
                    "price": store_product["salePrice"],
                    "price_cost": store_product["listPrice"],
                    "stock_quantity": store_product["stockQuantity"],
                    "unit_label": store_product["measurementUnit"]["String"] if store_product["measurementUnit"]["String"] else "UN",
                    "unit_quantity": 1,
                    "view": [],
                }

                for attribute in product['attributes']:
                    # create attributes of cor for opabox
                    if attribute['name'].lower() == "cor":
                        if not "cor" in presentations:
                            presentations['cor'] = {
                                "id": str(attribute['id']),
                                "name": "Cor",
                                "options": []
                            }
                    if not str(attribute['values'][0]['id']) in [c['id'] for c in presentations['cor']['options']]:
                        option = {
                            "id": str(attribute['values'][0]['id']),
                            "label": attribute['values'][0]['value']
                        }
                        presentations['cor']['options'].append(option)
                        product_view['view'].append({"option_id": option['id'], 'presentation_id': presentations['cor']['id']})
                    else:
                        option = {}

                        for op in presentations['cor']['options']:
                            if str(attribute['values'][0]['id']) == str(op['id']):
                                option = op

                        product_view['view'].append({"option_id": option['id'], 'presentation_id': presentations['cor']['id']})

                    # create attributes of size for opabox
                    if attribute['name'].lower() == "tamanho":
                        size = attribute['values'][0]['value']
                        if not "tamanho" in presentations:
                            presentations['tamanho'] = {
                                "id": str(attribute['id']),
                                "name": "tamanho",
                                "options": []
                            }

                        if not str(attribute['values'][0]['id']) in [c['id'] for c in presentations['tamanho']['options']]:
                            option = {
                                "id": str(attribute['values'][0]['id']),
                                "label": str(attribute['values'][0]['value'])
                            }
                            presentations['tamanho']['options'].append(option)
                            product_view['view'].append({"option_id": str(option['id']), 'presentation_id': str(presentations['tamanho']['id'])})
                        else:
                            option = {}

                            for op in presentations['tamanho']['options']:
                                if str(attribute['values'][0]['id']) == op['id']:
                                    option = op
                            product_view['view'].append({"option_id": str(option['id']), 'presentation_id': str(presentations['tamanho']['id'])})

                payload['product_views'].append(product_view)

            else:
                product_view = {
                        "active": True,
                        "id": str(store_product["id"]),
                        "name": str(store_product["productName"]["String"]),
                        "order": 0,
                        "photos": None,
                        "price": store_product["salePrice"],
                        "price_cost": store_product["listPrice"],
                        "stock_quantity": store_product["stockQuantity"],
                        "unit_label": store_product["measurementUnit"]["String"] if store_product["measurementUnit"]["String"] else "UN",
                        "unit_quantity": 1,
                        "view": [],
                    }

                payload['product_views'].append(product_view)

            if store_product['eanProduct']['String']:
                product_view.update({
                    "ean": str(store_product['eanProduct']['String'])
                })
                product_view.update({
                    "sku": str(store_product['productCode']['String'])
                })
            else:
                # product_view.update({
                #     "ean": str(a['productCode']['String'])
                # })
                product_view.update({
                    "sku": str(store_product['productCode']['String'])
                })

            if categ and categ_id:
                payload.update({
                    "category_id": str(categ_id),
                    "category_label": str(categ)
                })

        return payload

    @classmethod
    def make_update_product(self, store_product='', parent='', product=''):
        pass

    @classmethod
    def create_products(self, server_url, company, api_token='', products=[]):
        # create headers
        headers = {'Content-Type': 'Application/json'}

        # create url
        url = f'{server_url}/prod/v2/company/{company}/products?api_token={api_token}'

        for product in products:
            # do request to create a product
            logging.info(f'Criando produto na opabox...')
            r = requests.put(url, headers=headers, data=json.dumps([product]))

            if r.status_code == 200:
                logging.info('Sucessfull create product in opabox')
            else:
                logging.error(f'Error at created product in opabox {r.status_code} - {r.text}')

        return r.status_code

    @classmethod
    def update_product(self, server_url, company, api_token='', products=[], pagination=50):
        # create headers
        headers = {'Content-Type': 'Application/json'}
        
        for i in range(0, len(products), pagination):
            # create url
            url = f'{server_url}/prod/v2/company/{company}/products_price_stock?api_token={api_token}'

            # create product payload
            payload_product = json.dumps(products[i:i+pagination], ensure_ascii=False)

            # do request to create a product
            r = requests.post(url, headers=headers, data=payload_product)

            # # log
            logging.info(f'OpaBox update products {r.status_code}:{r.content} - from {i} to {i+pagination if i+pagination<len(products) else len(products)}')
