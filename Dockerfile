FROM frappe/erpnext:v15.121.0

USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-jre-headless \
    xmlsec1 \
    && rm -rf /var/lib/apt/lists/*

USER frappe
COPY --chown=frappe:frappe apps/ksa_compliance /home/frappe/frappe-bench/apps/ksa_compliance
RUN /home/frappe/frappe-bench/env/bin/pip install --no-cache-dir -e /home/frappe/frappe-bench/apps/ksa_compliance \
    && cd /home/frappe/frappe-bench && bench build --app ksa_compliance
