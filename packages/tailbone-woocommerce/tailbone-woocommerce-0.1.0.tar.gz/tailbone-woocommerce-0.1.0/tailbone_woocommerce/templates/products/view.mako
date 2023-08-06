## -*- coding: utf-8; -*-
<%inherit file="tailbone:templates/products/view.mako" />

<%def name="object_helpers()">
  ${parent.object_helpers()}
  ${self.render_xref_helper()}
</%def>

<%def name="render_xref_store_button()">
  <b-button type="is-primary"
            % if woocommerce_store_url:
            tag="a" href="${woocommerce_store_url}" target="_blank"
            % else:
            disabled title="${woocommerce_store_why_no_url}"
            % endif
            >
    View in WooCommerce Store
  </b-button>
</%def>

<%def name="render_xref_admin_button()">
  <b-button type="is-primary"
            % if woocommerce_admin_url:
            tag="a" href="${woocommerce_admin_url}" target="_blank"
            % else:
            disabled title="${woocommerce_admin_why_no_url}"
            % endif
            >
    View in WooCommerce Admin
  </b-button>
</%def>

<%def name="render_xref_helper()">
  <div class="object-helper">
    <h3>Cross-Reference</h3>
    <div class="object-helper-content">
      ${self.render_xref_store_button()}
      ${self.render_xref_admin_button()}
    </div>
  </div>
</%def>

<%def name="extra_main_fields(form)">
  ${parent.extra_main_fields(form)}
  ${self.extra_main_fields_woocommerce(form)}
</%def>

<%def name="extra_main_fields_woocommerce(form)">
  ${form.render_field_readonly('woocommerce_id')}
</%def>

${parent.body()}
