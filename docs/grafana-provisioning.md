Production SRE Lab — Grafana provisioning bundle

Purpose:
- Add one separate, stable Grafana datasource Prometheus-SRE-Lab-IaC (uid prometheus-sre-lab).
- Provision the existing Infrastructure Overview dashboard by UID srelab-infra-01.
- Preserve the manually created datasource called prometheus. It is not deleted.
- Do NOT overwrite ansible/playbooks/grafana-server.yml or the Grafana GPG public key.

WARNINGS:
- Provisioning will update the already imported dashboard with UID srelab-infra-01.
- Dashboard editing in Grafana UI will become read-only (allowUiUpdates: false). Future changes should be made in the JSON stored in Git.
- Restarting Grafana may briefly interrupt the SSH tunnel web UI, not Prometheus, PostgreSQL, or FastAPI.
- Export any UI changes before applying if you have modified the imported dashboard.

Suggested path on sre-control: /home/sre/sre-cloud-platform
From that repo root:
  cd ansible
  ansible-playbook --syntax-check playbooks/grafana-provision.yml
  ansible-playbook playbooks/grafana-provision.yml
  ansible-playbook playbooks/grafana-provision.yml  # repeat for idempotence (changed=0)

After apply:
- Refresh Dashboard in Grafana; existing URL should still work.
- Check default data source is Prometheus-SRE-Lab-IaC.
- Confirm 14 panels render and Service Health shows 7 targets.
- Do not delete original manually created datasource until the new one is confirmed working.
- Verify new files with git status; commit only reviewed files, do not add *.bak, secrets, credentials, or private keys.
