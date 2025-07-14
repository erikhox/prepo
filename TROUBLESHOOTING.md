## GitHub Actions Troubleshooting Checklist

### 1. Check Repository Settings
1. Go to your GitHub repository
2. Click **Settings** tab
3. Click **Actions** in the left sidebar
4. Under **Actions permissions**, ensure it's set to:
   - "Allow all actions and reusable workflows" OR
   - "Allow select actions and reusable workflows" (with appropriate selections)

### 2. Verify Branch Name
The workflow triggers on pushes to `main` and `develop` branches.
- If your default branch is `master`, update the workflow file
- Check which branch you're pushing to

### 3. Commit and Push the Fixed Workflow
```bash
git add .github/workflows/ci-cd.yml
git commit -m "Fix GitHub Actions workflow"
git push origin main  # or your default branch
```

### 4. Check Actions Tab
1. Go to your repository on GitHub
2. Click the **Actions** tab
3. Look for any workflow runs or error messages

### 5. Force Trigger (for testing)
You can manually trigger the workflow by:
1. Go to Actions tab
2. Select the "CI/CD Pipeline" workflow
3. Click "Run workflow" button (if available)

### 6. Check YAML Syntax
The workflow file should now be valid, but you can verify at:
https://yamlchecker.com/

### 7. Verify File Path
Ensure the file is exactly at:
`.github/workflows/ci-cd.yml`

### 8. Organization Restrictions
If this is in an organization, check if:
- Actions are disabled for the organization
- There are security policies preventing workflows

Let me know what you find when checking these items!
