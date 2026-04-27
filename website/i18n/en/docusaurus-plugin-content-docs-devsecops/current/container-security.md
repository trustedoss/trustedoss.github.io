---
id: container-security
title: Container/Image Security
sidebar_label: container security
sidebar_position: 6
---

# Container/Image Security

## What is container security?

This is a security check that detects vulnerabilities in OS package and application dependencies included in container images, Dockerfile configuration errors, and secret exposure before deployment. Blocking the build phase is especially important because once the image is deployed, the same vulnerability will spread across all instances.

---

## Tool Comparison

| tools  | Features                           | Detection range             | License    |
| ------ | ---------------------------------- | --------------------------- | ---------- |
| Trivy  | All-in-one·Fast speed·Simple setup | Image·Filesystem·IaC·Secret | Apache-2.0 |
| Grype  | SBOM integration optimization      | Image/File System           | Apache-2.0 |
| Dockle | Checking Dockerfile best practices | Image Settings              | Apache-2.0 |

We recommend Trivy as a single container security tool, and if you are already using grype in your SCA pipeline, image scanning can also be unified with grype.

---

## Trivy settings

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
      - uses: actions/checkout@v4

      - name: Build image
        run: docker build -t myapp:${{ github.sha }} .

      - name: Scan image — vulnerability
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: myapp:${{ github.sha }}
          format: table
          exit-code: 1
          severity: HIGH,CRITICAL
          ignore-unfixed: true

      - name: Scan image — secret
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: myapp:${{ github.sha }}
          scanners: secret
          exit-code: 1

      - name: Upload SBOM
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: myapp:${{ github.sha }}
          format: cyclonedx
          output: sbom.cdx.json

      - uses: actions/upload-artifact@v4
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
  image: aquasec/trivy:latest
  services:
    - docker:dind
  variables:
    DOCKER_HOST: tcp://docker:2376
    IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  script:
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

Exclude unfixable vulnerabilities with :::info ignore-unfixed option
Vulnerabilities that are not yet patched upstream cannot be fixed by the development team, so excluding them allows us to focus on actionable notifications.
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

1. **Use minimal base image:** Select `alpine`·`distroless` instead of `ubuntu`. Fewer packages reduce your vulnerability surface area.
2. **Prohibit root execution:** Specify a non-root user with the `USER` command. Root execution magnifies the damage when a container escapes.
3. **Multi-stage build:** Exclude build tools and source code from the final image. Image size reduction and attack surface reduction are achieved simultaneously.
4. **No secret ARG/ENV:** Do not pass secrets as build arguments or environment variables. It remains as plain text in the image layer.
5. **Version Fixed:** Specify tags like `FROM ubuntu:22.04`. When using `latest`, unexpected vulnerabilities may be introduced.

---

## Next steps

- Infrastructure code security: [IaC security](./iac-security)
- Full pipeline integration: [Pipeline Design](./pipeline-design)
- Continuous monitoring of images after distribution: [Monitoring·Automatic Correction](./monitoring)
