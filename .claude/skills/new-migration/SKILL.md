---
name: new-migration
description: Scaffolds a new numbered FluentMigrator migration class in src/Migrations/ with the correct version timestamp and Up/Down stubs pre-filled. Ensures consistent naming and structure across all migrations.
disable-model-invocation: true
argument-hint: [description] e.g. AddPlaylistsTable
---

You are scaffolding a new FluentMigrator migration for the Jamtrack Radio database.

If $ARGUMENTS is provided, use it as the migration description (PascalCase, e.g. `AddPlaylistsTable`). Otherwise, ask:
- What does this migration do? (e.g. `CreateUsersTable`, `AddGenreColumnToTracks`, `DropLegacyTokensTable`)

Use `$DESCRIPTION` to represent the migration description throughout.

---

## Step 1 — Generate Version Timestamp

The migration version is a timestamp in `YYYYMMDDHHmmss` format, based on the current UTC time.

```bash
date -u +"%Y%m%d%H%M%S"
```

Use the output as `$VERSION`. Example: `20260320143000`

---

## Step 2 — Create the Migration File

Create `src/Migrations/Migration_$VERSION_$DESCRIPTION.cs`:

```csharp
using FluentMigrator;

namespace Migrations;

[Migration($VERSION)]
public sealed class $DESCRIPTION : Migration
{
  public override void Up()
  {
    // TODO: implement schema change
    // Examples:
    //
    // Create.Table("table_name")
    //   .WithColumn("id").AsGuid().PrimaryKey()
    //   .WithColumn("name").AsString(255).NotNullable()
    //   .WithColumn("created_at").AsDateTimeOffset().NotNullable();
    //
    // Alter.Table("table_name")
    //   .AddColumn("new_column").AsString(100).Nullable();
    //
    // Create.Index("ix_table_column")
    //   .OnTable("table_name")
    //   .OnColumn("column_name").Ascending();
    //
    // Create.ForeignKey("fk_table_other_id")
    //   .FromTable("table_name").ForeignColumn("other_id")
    //   .ToTable("other_table").PrimaryColumn("id");
  }

  public override void Down()
  {
    // TODO: implement rollback — reverse everything in Up()
    // Examples:
    //
    // Delete.Table("table_name");
    //
    // Delete.Column("new_column").FromTable("table_name");
    //
    // Delete.Index("ix_table_column").OnTable("table_name");
    //
    // Delete.ForeignKey("fk_table_other_id").OnTable("table_name");
  }
}
```

---

## Step 3 — Migration Rules

Apply these rules when filling in the `Up()` and `Down()` methods:

| Rule | Detail |
|---|---|
| Use FluentMigrator fluent API | `Create.Table`, `Alter.Table`, `Delete.Table` — never raw SQL in migrations |
| Always implement `Down()` | Every migration must be reversible — `Down()` must undo exactly what `Up()` does |
| UUID primary keys | Use `.AsGuid().PrimaryKey()` |
| Timestamps | Use `.AsDateTimeOffset().NotNullable()` for `created_at` / `updated_at` |
| Foreign keys | Always create an index on the FK column |
| String lengths | Always set an explicit max length — never `.AsString()` without a size |
| Unique constraints | Use `.Unique()` on the column or `Create.UniqueConstraint()` |
| No data migrations | Data changes go in a separate migration from schema changes |
| Backward compatibility | Additive changes (new nullable column, new table) are safe. Destructive changes (drop column, rename) require a deprecation migration strategy |

---

## Step 4 — Verify

```bash
# Dry-run to confirm the migration compiles
dotnet build src/Migrations

# Apply the migration against the local dev DB
dotnet run --project src/Migrations -- \
  --connection "Host=localhost;Database=jamtrack_dev;Username=jamtrack;Password=<pwd>"

# Verify in psql
psql -h localhost -U jamtrack -d jamtrack_dev -c "\dt"
```

---

After creating the migration, ask:
- Should we apply the migration to the local dev DB now?
- Is a corresponding down migration needed immediately for testing rollback?
- Ready to continue with implementation? Run `/implement`
