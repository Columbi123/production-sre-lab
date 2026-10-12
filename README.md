# Production SRE Lab

**Cloud infrastructure and Site Reliability Engineering portfolio project.**

A production-inspired infrastructure lab built on MWS Cloud Platform to practice Infrastructure as Code, automation, container orchestration, monitoring, incident response, and reliability engineering.

## Technology Stack

- **Cloud:** MWS Cloud Platform
- **Infrastructure as Code:** Terraform
- **Configuration Management:** Ansible (planned)
- **Containers:** Docker (planned)
- **Orchestration:** Kubernetes (planned)
- **Monitoring:** Prometheus, Grafana, Alertmanager (planned)
- **Version Control:** Git and GitHub
- **Operating System:** Ubuntu Server 24.04 LTS

## Current Infrastructure

| Component | Description | Status |
|---|---|---|
| VPC | `sre-lab-vpc` | Deployed, imported into Terraform |
| Management Subnet | `10.10.10.0/24` | Deployed, imported into Terraform |
| Control VM | `sre-control` | Deployed, referenced as a Data Source |
| Terraform State | MWS Object Storage | Configured |
| Git Repository | GitHub | Configured |
| Application Infrastructure | To be provisioned | Planned |
| Monitoring Infrastructure | Prometheus and Grafana | Planned |

## Project Roadmap

- [x] Set up MWS Cloud Platform
- [x] Configure VPC and management subnet
- [x] Deploy management VM
- [x] Install Terraform and Ansible
- [x] Configure remote Terraform State
- [x] Import existing network resources into Terraform
- [x] Initialize GitHub repository
- [ ] Automate VM provisioning with Terraform
- [ ] Configure servers with Ansible
- [ ] Deploy containerized application
- [ ] Configure Kubernetes
- [ ] Implement monitoring and alerting
- [ ] Introduce CI/CD workflows
- [ ] Implement SRE reliability tests and incident simulations

## Repository Structure

- `terraform/` — Infrastructure as Code
- `ansible/` — Configuration management
- `docs/` — Technical documentation and architecture

## Security and Operational Notes

- Secrets and private SSH keys must not be committed to Git.
- Terraform State is stored remotely in MWS Object Storage with versioning enabled.
- S3 State Locking is currently disabled due to an observed compatibility issue. Terraform operations must be serialized until a reliable locking mechanism is implemented.
- Infrastructure changes must be reviewed with `terraform plan` before applying.

## Project Goal

Build a reproducible infrastructure environment demonstrating practical SRE/DevOps competencies, including automation, observability, incident management, and infrastructure reliability.

**Status:** Active development — Cloud Foundation completed.
