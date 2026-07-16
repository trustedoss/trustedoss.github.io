---
id: container-security
title: Container/Image Security
sidebar_label: Container Security
sidebar_position: 6
---

# Container/Image Security

## What is container security?

Container security scanning detects vulnerabilities in the OS packages and application dependencies bundled into a container image, along with Dockerfile misconfigurations and exposed secrets, before deployment. Blocking these at the build stage is especially important because once an image is deployed, the same vulnerability propagates to every instance.

:::tip The configuration below is an example — a fully working implementation lives in the reference repository
The YAML and commands on this page are examples that show the essentials. For a complete, copy-and-run pipeline (including policy files and a sample app), see the [Best Practice repository](/ai-coding/best-practice-repo).
:::

---

## Tool Comparison

| Tool   | Features                         | Detection range             | License    |
| ------ | -------------------------------- | --------------------------- | ---------- |
| Trivy  | All-in-one, fast, simple setup   | Image·Filesystem·IaC·Secret | Apache-2.0 |
| Grype  | Optimized for SBOM integration   | Image/Filesystem            | Apache-2.0 |
| Dockle | Checks Dockerfile best practices | Image configuration         | Apache-2.0 |

We recommend Trivy as a single container security tool. If you already use Grype in your SCA pipeline, you can unify image scanning on Grype as well.

---

## Trivy setup

### Basic usage

```bash
# scan local image
trivy image myapp:latest

# scan filesystem (before build)
trivy fs .

# Generate SBOM
trivy image --format cyclonedx myapp:latest \
  -o sbom.cdx.json

# Severity filter
trivy image --severity HIGH,CRITICAL myapp:latest
```

### GitHub Actions

```yaml
# .github/workflows/container-security.yml

name: Container Security — Trivy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  trivy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7

      - name: Build image
        run: docker build -t myapp:${{ github.sha }} .

      - name: Scan image — vulnerability
        uses: aquasecurity/trivy-action@0.36.0
        with:
          image-ref: myapp:${{ github.sha }}
          format: table
          exit-code: 1
          severity: HIGH,CRITICAL
          ignore-unfixed: true

      - name: Scan image — secret
        uses: aquasecurity/trivy-action@0.36.0
        with:
          image-ref: myapp:${{ github.sha }}
          scanners: secret
          exit-code: 1

      - name: Upload SBOM
        uses: aquasecurity/trivy-action@0.36.0
        with:
          image-ref: myapp:${{ github.sha }}
          format: cyclonedx
          output: sbom.cdx.json

      - uses: actions/upload-artifact@v7
        with:
          name: container-sbom-${{ github.sha }}
          path: sbom.cdx.json
          retention-days: 90
```

### GitLab CI

```yaml
# .gitlab-ci.yml (container-security job section)

container-security:
  stage: test
  image: docker:27
  services:
    - docker:27-dind
  variables:
    DOCKER_TLS_CERTDIR: '/certs'
    IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  script:
    # the docker image does not include trivy, so install it
    - apk add --no-cache curl
    - curl -sSfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh
      | sh -s -- -b /usr/local/bin
    - docker build -t $IMAGE_TAG .
    # vulnerability scan
    - trivy image
      --severity HIGH,CRITICAL
      --exit-code 1
      --ignore-unfixed
      $IMAGE_TAG
    # secret scan
    - trivy image
      --scanners secret
      --exit-code 1
      $IMAGE_TAG
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

---

## Trivy policy file

:::info Exclude unfixable vulnerabilities with the ignore-unfixed option
Vulnerabilities not yet patched upstream cannot be fixed by the development team, so excluding them lets you focus on actionable findings.
:::

```yaml
# .trivyignore.yaml

vulnerabilities:
  - id: CVE-2023-XXXXX
    paths:
      - usr/lib/some-lib
    statement: 'Path unused in container — security team approved 2024-02-01'

secrets:
  - id: aws-access-key-id
    paths:
      - test/fixtures/dummy.env
```

---

## Dockerfile security best practices

1. **Use a minimal base image:** Choose `alpine` or `distroless` over `ubuntu`. Fewer packages mean a smaller vulnerability surface.
2. **Avoid running as root:** Specify a non-root user with the `USER` instruction. Running as root amplifies the damage if a container is compromised.
3. **Multi-stage builds:** Keep build tools and source code out of the final image. This reduces both image size and attack surface at once.
4. **No secrets in ARG/ENV:** Never pass secrets as build arguments or environment variables. They persist as plain text in the image layers.
5. **Pin versions:** Use explicit tags like `FROM ubuntu:22.04`. Using `latest` can silently introduce unexpected vulnerabilities.

---

:::note Pin your versions
Trivy's repository was hijacked in 2026-03 and malicious versions were briefly published (since recovered). Pin action and image references to version tags (ideally commit digests) instead of moving refs like `latest` or `master`.
:::

:::note
The browser-based result analyzers offered on the SCA, SAST, secret detection, and IaC pages do not yet exist for this topic.
If you need help interpreting results, feed the SBOM generated by Trivy (sbom.cdx.json) into the analyzer on the [SCA page](./sca).
:::

## Next steps

- Infrastructure code security: [IaC security](./iac-security)
- Full pipeline integration: [Pipeline Design](./pipeline-design)
- Continuous monitoring of images after deployment: [Monitoring and Automated Remediation](./monitoring)
