# syntax=docker/dockerfile:1
# Frappe + ERPNext + Frappe HR (version-16) with the erpnext_armenian app.
# Build context: repository root.  Based on frappe_docker images/layered/Containerfile (MIT).
ARG FRAPPE_BRANCH=version-16

FROM frappe/build:${FRAPPE_BRANCH} AS builder
ARG FRAPPE_BRANCH=version-16
USER frappe
COPY --chown=frappe:frappe docker/apps.json /opt/frappe/apps.json
RUN bench init --apps_path=/opt/frappe/apps.json \
      --frappe-branch=${FRAPPE_BRANCH} \
      --frappe-path=https://github.com/frappe/frappe \
      --no-procfile --no-backups --skip-redis-config-generation --verbose \
      /home/frappe/frappe-bench && \
    cd /home/frappe/frappe-bench && echo "{}" > sites/common_site_config.json

# --- erpnext_armenian (this layer rebuilds in seconds when only translations change) ---
COPY --chown=frappe:frappe pyproject.toml README.md LICENSE /home/frappe/frappe-bench/apps/erpnext_armenian/
COPY --chown=frappe:frappe erpnext_armenian /home/frappe/frappe-bench/apps/erpnext_armenian/erpnext_armenian
COPY --chown=frappe:frappe docker/compile_mo.py /tmp/compile_mo.py
RUN cd /home/frappe/frappe-bench && \
    (env/bin/python -m pip install --quiet --no-deps -e apps/erpnext_armenian 2>/dev/null || \
     echo "/home/frappe/frappe-bench/apps/erpnext_armenian" > "$(env/bin/python -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])')/erpnext_armenian.pth") && \
    env/bin/python -c "import erpnext_armenian; print('erpnext_armenian', erpnext_armenian.__version__)" && \
    ls -1 apps > sites/apps.txt && \
    env/bin/python /tmp/compile_mo.py && \
    find apps -mindepth 1 -path "*/.git" | xargs rm -fr && \
    chmod -R g=u /home/frappe/frappe-bench

FROM frappe/base:${FRAPPE_BRANCH} AS backend
USER frappe
COPY --from=builder --chown=frappe:0 /home/frappe/frappe-bench /home/frappe/frappe-bench
WORKDIR /home/frappe/frappe-bench
RUN chmod g=u /home/frappe/frappe-bench && \
    cp -r /home/frappe/frappe-bench/sites/assets /home/frappe/frappe-bench/assets && \
    rm -rf /home/frappe/frappe-bench/sites/assets
VOLUME [ "/home/frappe/frappe-bench/sites", "/home/frappe/frappe-bench/logs" ]
USER root
COPY docker/resources/main-entrypoint.sh /usr/local/bin/entrypoint.sh
COPY docker/resources/start.sh /usr/local/bin/start.sh
RUN sed -i 's/\r$//' /usr/local/bin/entrypoint.sh /usr/local/bin/start.sh && chmod 755 /usr/local/bin/entrypoint.sh /usr/local/bin/start.sh
USER frappe
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["start.sh"]
