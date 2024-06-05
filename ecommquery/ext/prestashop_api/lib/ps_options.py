

class PSOptionValue:
    def __init__(self, raw):
        pass

class PSOption:
    def __init__(self, raw):
        pass

    @staticmethod
    def getProductOptionsList(raw):
        if not 'product_feature' in raw['product_options']:
            return []

        raw_options = raw['product_options']['product_feature']

        # just one element
        if isinstance(raw_options, dict):
            return [raw_options]

        return raw_options

    @staticmethod
    def getProductOptionValuesList(raw):
        if not 'product_option_value' in raw['product_option_values']:
            return []

        raw_opt_vals = raw['product_option_values']['product_option_value']

        # if only one element is defined it can be not enclosed within list,
        # add the list around for iterations to work
        if isinstance(raw_opt_vals, dict):
            return [raw_opt_vals]

        return raw_opt_vals
