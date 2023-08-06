# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2021 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Product Views
"""

from sqlalchemy import orm

from rattail_woocommerce.config import woocommerce_admin_product_url

from tailbone.views import products as base


class ProductView(base.ProductsView):
    """
    Master view for the Product class.
    """
    labels = {
        'woocommerce_id': "WooCommerce ID",
    }

    @property
    def form_fields(self):
        fields = super(ProductView, self).form_fields
        return self.woocommerce_add_form_fields(fields)

    def woocommerce_add_form_fields(self, fields):
        fields.extend([
            'woocommerce_id',
        ])
        return fields

    def query(self, session):
        query = super(ProductView, self).query(session)
        return self.woocommerce_modify_query(query)

    def woocommerce_modify_query(self, query):
        model = self.model
        return query.outerjoin(model.WooProductExtension)

    def configure_grid(self, g):
        super(ProductView, self).configure_grid(g)
        self.woocommerce_configure_grid(g)

    def woocommerce_configure_grid(self, g):
        model = self.model
        g.set_filter('woocommerce_id', model.WooProductExtension.woocommerce_id)

    def configure_form(self, f):
        super(ProductView, self).configure_form(f)
        self.woocommerce_configure_form(f)

    def woocommerce_configure_form(self, f):
        f.set_required('woocommerce_id', False)
        if self.creating:
            f.remove('woocommerce_id')

    def get_version_child_classes(self):
        classes = super(ProductView, self).get_version_child_classes()
        return self.woocommerce_add_version_classes(classes)

    def woocommerce_add_version_classes(self, classes):
        model = self.model
        classes.extend([
            model.WooProductExtension,
        ])
        return classes

    def template_kwargs_view(self, **kwargs):
        kwargs = super(ProductView, self).template_kwargs_view(**kwargs)
        return self.woocommerce_template_kwargs_view(**kwargs)

    def get_woo_cached_product(self, product):
        """
        Tries to identify the WooCacheProduct for the given Rattail Product.
        """
        woo_cached = None

        if product.woocommerce_cache_product:
            # we have an official link between rattail and woo
            woo_cached = product.woocommerce_cache_product

        elif product.item_id:
            # try to find matching woo product, even though not linked
            model = self.rattail_config.get_model()
            try:
                woo_cached = self.Session.query(model.WooCacheProduct)\
                                         .filter(model.WooCacheProduct.sku == product.item_id)\
                                         .one()
            except orm.exc.NoResultFound:
                pass

        return woo_cached

    def woocommerce_template_kwargs_view(self, **kwargs):
        product = kwargs['instance']
        woo_cached = self.get_woo_cached_product(product)

        # WooCommerce Store URL
        store_url = why_not = None
        if woo_cached:
            store_url = woo_cached.permalink
        else:
            why_not = "WooCommerce cache product not found"
        kwargs['woocommerce_store_url'] = store_url
        kwargs['woocommerce_store_why_no_url'] = why_not

        # WooCommerce Admin URL
        admin_url = why_not = None
        woo_id = woo_cached.id if woo_cached else product.woocommerce_id
        if woo_id:
            admin_url = woocommerce_admin_product_url(self.rattail_config,
                                                      woo_id)
            if not admin_url:
                why_not = "WooCommerce Admin URL is not configured"
        else:
            why_not = "Product is not known to exist in WooCommerce"
        kwargs['woocommerce_admin_url'] = admin_url
        kwargs['woocommerce_admin_why_no_url'] = why_not

        return kwargs


def includeme(config):

    # TODO: getting pretty tired of copy/pasting this extra config...
    config.add_route('products.autocomplete', '/products/autocomplete')
    config.add_view(base.ProductsAutocomplete, route_name='products.autocomplete',
                    renderer='json', permission='products.list')

    # TODO: getting pretty tired of copy/pasting this extra config...
    config.add_route('products.print_labels', '/products/labels')
    config.add_view(base.print_labels, route_name='products.print_labels',
                    renderer='json', permission='products.print_labels')

    ProductView.defaults(config)
