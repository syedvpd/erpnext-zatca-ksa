FROM frappe/erpnext:version-15

USER frappe
WORKDIR /home/frappe/frappe-bench

# Install ksa_compliance
RUN bench get-app --resolve-deps --branch master https://github.com/lavaloon-eg/ksa_compliance.git

# Build assets and ensure baked assets are updated
RUN bench build --app ksa_compliance && \
    cp -r /home/frappe/frappe-bench/sites/assets/* /home/frappe/frappe-bench/assets/ 2>/dev/null || true
