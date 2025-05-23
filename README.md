# naf-temporal-2025

This repository accompanies the **"Transforming Network Automation with Temporal"** presentation delivered at the Network Automation Forum, Prague, May 2025. It provides a Temporal workflow for network automation using Containerlab. You can try it out easily in GitHub Codespaces to explore configuration management automation via Temporal workflows.

As mentioned during the presentation, the Temporal workflow will conclude with a codeword which will be a concatenation of strings from each activity. To win a $20 gift card, participants must identify and collect substrings returned by each activity and share it with me via naf slack or in-person!

> **Note:** The `clab.yaml` topology file and device configurations are sourced from the [srl-labs telemetry lab repository](https://github.com/srl-labs/srl-telemetry-lab).

## Overview

This workflow demonstrates network automation with Temporal by pushing BGP configuration to `spine1` to establish a BGP session between `spine1` and `leaf1`.

## Running the Setup

### Prerequisites

- Linux environment (GitHub Codespaces recommended)  
- `sudo` privileges  
- Internet access to download software packages  

### Network Simulation Setup

We use ContainerLab to simulate the network environment.

```bash
# Deploy the network topology
sudo containerlab deploy -t clab.yaml
```

### Install temporal

```bash
wget -O temporal.tar.gz "https://temporal.download/cli/archive/latest?platform=linux&arch=amd64"
tar -xzf temporal.tar.gz
sudo mv temporal /usr/local/bin/
```

### Run Temporal Server

```bash
temporal server start-dev
```

Temporal UI will running on `http://localhost:8233`\
If you are using github codespace, you can go to ports tab and click on the forwarded address link for port 8233.

### Install uv to manage dependencies and virtual environment

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Run Temporal Worker

```bash
uv run run_worker.py
```

### Run Temporal Workflow

```bash
uv run run_workflow.py
```

> **Note**: While running the workflow, you may see exceptions related to BGP session verification. This is expected because the workflow retries with exponential backoff while waiting for the BGP session to establish. The workflow will complete either when verification succeeds or when the maximum number of retries is reached. If verification succeeds, run_workflow.py will print the final output; otherwise, the workflow will fail.

### Verify BGP Session

```bash
show network-instance protocols bgp neighbor
```

### Cleanup

```bash
sudo containerlab destroy -t clab.yaml
```

> **Note**: If you're using GitHub Codespaces, remember to delete your workspace when finished to avoid charges beyond your free tier allocation.

## References

- [Temporal Documentation](https://docs.temporal.io/)
- [Containerlab Documentation](https://containerlab.dev/)
- [uv CLI Tool](https://astral.sh/uv/)
