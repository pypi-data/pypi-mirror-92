shopify-multipass
=================

Shopify Multipass module for Python



[Shopify](http://shopify.com) provides a mechanism for single sign-on known as Multipass.  Multipass uses an AES encrypted JSON hash and multipassify provides functions for generating tokens

More details on Multipass with Shopify can be found [here](http://docs.shopify.com/api/tutorials/multipass-login).

## Installation
```sh
$ pip install shopify-multipass
```

## Usage

To use Multipass an Enterprise / Plus plan is required. The Multipass secret can be found in your shop Admin (Settings > Checkout > Customer Accounts).
Make sure "Accounts are required" or "Accounts are optional" is selected and Multipass is enabled.

```python
# Construct the Multipassify encoder
from multipass import Multipass

multipass = Multipass('SHOPIFY MULTIPASS SECRET');

# Create your customer data hash
customerData = {'email': 'test@example.com', 'return_to': 'http://some.url'};

# Generate a Shopify multipass URL to your shop
url = multipass.generateURL(customerData, 'yourstorename.myshopify.com');

# Generates a URL like:  https://yourstorename.myshopify.com/account/login/multipass/<MULTIPASS-TOKEN>
```

## References

[multipassify](https://github.com/beaucoo/multipassify)
