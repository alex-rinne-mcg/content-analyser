# GitHub Setup for N8N Workflow Management

This guide explains how to use GitHub for version control and automated deployment of the N8N workflow.

## Initial Setup

### 1. Create GitHub Repository

1. Go to [GitHub](https://github.com) and create a new repository
2. Name it: `n8n-zzuper-workflow` (or your preferred name)
3. **Don't** initialize with README (we already have one)

### 2. Connect Local Repository to GitHub

```bash
# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/n8n-zzuper-workflow.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 3. Add All Files

```bash
# Add all relevant files
git add .
git commit -m "Add workflow and documentation"
git push
```

## Workflow Management

### Manual Workflow Updates

1. **Make changes** to `zzuper-meta-analysis-workflow.json` locally
2. **Commit changes**:
   ```bash
   git add zzuper-meta-analysis-workflow.json
   git commit -m "Update workflow: [description of changes]"
   git push
   ```
3. **Import in N8N**:
   - Download the updated JSON from GitHub
   - Or use the N8N API to update (see below)

### Automated Updates (Optional)

You can set up a GitHub Action to automatically update N8N when changes are pushed:

1. Create `.github/workflows/update-n8n.yml` (see below)
2. Add N8N API credentials as GitHub Secrets
3. Push changes trigger automatic N8N update

## GitHub Actions Setup

### Prerequisites

- N8N API Key
- N8N Base URL
- Workflow ID

### Create GitHub Action

Create `.github/workflows/update-n8n.yml`:

```yaml
name: Update N8N Workflow

on:
  push:
    paths:
      - 'zzuper-meta-analysis-workflow.json'
    branches:
      - main

jobs:
  update-n8n:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Update N8N Workflow
        run: |
          curl -X PUT \
            -H "X-N8N-API-KEY: ${{ secrets.N8N_API_KEY }}" \
            -H "Content-Type: application/json" \
            -d @zzuper-meta-analysis-workflow.json \
            ${{ secrets.N8N_BASE_URL }}/api/v1/workflows/${{ secrets.N8N_WORKFLOW_ID }}
```

### Add GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Add the following secrets:
   - `N8N_API_KEY`: Your N8N API key
   - `N8N_BASE_URL`: Your N8N instance URL (e.g., `https://alexrinne.app.n8n.cloud`)
   - `N8N_WORKFLOW_ID`: Your workflow ID (e.g., `FOanQ6fVJVYw5jAG`)

## Benefits of GitHub Management

1. **Version Control**: Track all changes to the workflow
2. **Collaboration**: Multiple people can work on the workflow
3. **Rollback**: Easy to revert to previous versions
4. **Documentation**: Changes are documented in commit messages
5. **Automation**: Can automatically deploy to N8N
6. **Backup**: Workflow is safely stored in the cloud

## Best Practices

1. **Commit Messages**: Use descriptive commit messages
   - Example: `"Fix Get Insights node: Add response format options"`
   - Example: `"Update Meta API version to v21.0"`

2. **Branch Strategy**: Use branches for major changes
   ```bash
   git checkout -b feature/new-node
   # Make changes
   git commit -m "Add new node"
   git push origin feature/new-node
   # Create pull request on GitHub
   ```

3. **Regular Backups**: Push changes regularly
   ```bash
   git add .
   git commit -m "Backup: Current workflow state"
   git push
   ```

4. **Tag Releases**: Tag stable versions
   ```bash
   git tag -a v1.0.0 -m "Stable workflow version"
   git push origin v1.0.0
   ```

## Troubleshooting

### Git Authentication Issues

If you get authentication errors:
```bash
# Use personal access token instead of password
git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/n8n-zzuper-workflow.git
```

### Merge Conflicts

If you have conflicts:
```bash
# Pull latest changes
git pull origin main

# Resolve conflicts in your editor
# Then commit
git add .
git commit -m "Resolve merge conflicts"
git push
```

## Next Steps

1. ✅ Initialize git repository (done)
2. ⬜ Create GitHub repository
3. ⬜ Connect local repo to GitHub
4. ⬜ Push initial files
5. ⬜ (Optional) Set up GitHub Actions for auto-deployment

