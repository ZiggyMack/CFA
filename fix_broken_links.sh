#!/bin/bash
# Broken Link Fix Script - CFA Repository
# Fixes DASHBOARD.md -> REPO_HEALTH_DASHBOARD.md
# Fixes 88MPH_PROTOCOL.md -> 88MPH.md

echo "🔧 CFA Broken Link Fixer"
echo "========================"
echo ""

# Counter for changes
dashboard_count=0
protocol_count=0

# Fix DASHBOARD.md references (but preserve REPO_HEALTH_DASHBOARD.md)
echo "📝 Fixing DASHBOARD.md references..."
for file in $(find docs -name "*.md" -type f); do
    if grep -q "DASHBOARD\.md" "$file" && ! grep -q "REPO_HEALTH_DASHBOARD\.md" "$file"; then
        # Simple cases: direct file references
        if grep -q "/docs/repository/DASHBOARD\.md" "$file"; then
            sed -i 's|/docs/repository/DASHBOARD\.md|/docs/repository/REPO_HEALTH_DASHBOARD.md|g' "$file"
            echo "  ✅ Fixed: $file"
            ((dashboard_count++))
        fi

        # Link text references like [DASHBOARD.md]
        if grep -q "\[DASHBOARD\.md\]" "$file"; then
            sed -i 's|\[DASHBOARD\.md\]|[REPO_HEALTH_DASHBOARD.md]|g' "$file"
            echo "  ✅ Fixed link text: $file"
            ((dashboard_count++))
        fi

        # DEPENDS_ON references
        if grep -q "DEPENDS_ON:.*DASHBOARD\.md" "$file"; then
            sed -i 's|DASHBOARD\.md|REPO_HEALTH_DASHBOARD.md|g' "$file"
            echo "  ✅ Fixed DEPENDS_ON: $file"
            ((dashboard_count++))
        fi
    fi
done

# Fix 88MPH_PROTOCOL.md references
echo ""
echo "📝 Fixing 88MPH_PROTOCOL.md references..."
for file in $(find docs -name "*.md" -type f); do
    if grep -q "88MPH_PROTOCOL\.md" "$file"; then
        # Replace path references
        sed -i 's|/docs/repository/librarian_tools/88MPH_PROTOCOL\.md|/88MPH.md|g' "$file"
        sed -i 's|docs/repository/librarian_tools/88MPH_PROTOCOL\.md|88MPH.md|g' "$file"
        sed -i 's|librarian_tools/88MPH_PROTOCOL\.md|../../../88MPH.md|g' "$file"

        # Replace general references (but be careful with context)
        sed -i 's|88MPH_PROTOCOL\.md|88MPH.md|g' "$file"

        echo "  ✅ Fixed: $file"
        ((protocol_count++))
    fi
done

echo ""
echo "✅ Fix Complete!"
echo "========================"
echo "📊 Summary:"
echo "  - DASHBOARD.md fixes: $dashboard_count files"
echo "  - 88MPH_PROTOCOL.md fixes: $protocol_count files"
echo ""
echo "🔍 Verification:"
echo "  Run these commands to verify:"
echo "  grep -r 'DASHBOARD\.md' docs/ | grep -v 'REPO_HEALTH_DASHBOARD.md' | wc -l"
echo "  grep -r '88MPH_PROTOCOL\.md' docs/ | wc -l"
