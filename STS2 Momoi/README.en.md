# Game King Momoi (STS2_Momoi)

Languages: [中文](README.md) | English

**Author QQ: 2631262742** (feel free to add for bug reports, suggestions or co-op issues)

A copyable, buildable RitsuLib mod template providing a general Godot/C# project layout, sample content, and static placeholder assets.

**What the template includes:**

- A `[ModInitializer]` entry point plus a minimal custom character (with character card pool, relic pool, and potion pool).
- Four starter strikes, four starter defends, and one starter relic as samples.
- Minimal static Godot placeholder scenes for the combat character, energy counter, character select background, merchant, and rest site.
- Placeholder PNG files copied from vanilla resources and renamed for the template. Replace them after copying.
- Basic English and Simplified Chinese localization files.
- A complete Godot project, export preset, mod manifest, and MSBuild scripts.

## Learning Resources

- Contact: **QQ 2631262742**. When reporting a bug, please include the mod version from `mods/STS2_Momoi` and the log file `%APPDATA%\SlayTheSpire2\logs\godot.log`.

- [STS2-RitsuLib](https://github.com/BAKAOLC/STS2-RitsuLib): the shared framework library for Slay the Spire 2 mods. This template uses it for content registration, character scaffolding, and Godot resource integration.
- [RitsuLib Documentation](https://github.com/GlitchedReme/SlayTheSpire2ModdingTutorials/tree/master/RitsuLib): tutorials and examples by file.
- [Slay the Spire 2 Modding Tutorials site](https://glitchedreme.github.io/SlayTheSpire2ModdingTutorials/index.html): the full tutorial site.
- Template Wiki (Rider-first): [Chinese Home](https://github.com/alkaid616/STS2_Momoi/wiki/Home) | [English Home](https://github.com/alkaid616/STS2_Momoi/wiki/Home-EN).

## Install and Use

You can get this project two ways: via the NuGet template (automatic rename), or by copying the directory manually.

### Option A: NuGet template (recommended)

```powershell
# Install the template
dotnet new install STS2.RitsuLib.ModTemplate

# Create a new mod
dotnet new ritsulibmod -n MyMod

# Uninstall the template
dotnet new uninstall STS2.RitsuLib.ModTemplate
```

`dotnet new ritsulibmod -n MyMod` generates a project called `MyMod` and renames `STS2_Momoi`, sample class names, sample resource file names, resource folders, manifest names, namespaces, and localization IDs to match the new name.

### Option B: manual copy

1. Copy the whole directory and rename it to your mod name.
2. Edit `STS2_Momoi.json` and update `id`, `name`, `author`, and `description`.
3. Edit `STS2_MomoiCode/Entry.cs` and update `ModId`.
4. For a full rename, also update the project name and namespace in `.csproj`, `.sln`, and `project.godot`.
5. Rename the resource directory `STS2_Momoi/` to your `ModId`, then update the related `Entry.ResPath` paths in code.

## Local Path Configuration

```powershell
Copy-Item .\local.props.template .\local.props
```

Set these values in `local.props` (the file is in `.gitignore`; do not commit it):

| Field | Description |
|---|---|
| `Sts2Dir` | Slay the Spire 2 install directory |
| `Sts2DataDir` | Game DLL directory, usually `$(Sts2Dir)/data_sts2_windows_x86_64` |
| `GodotExe` | MegaDot/Godot executable used to export the PCK |
| `RitsuLibDeployDir` | Local RitsuLib deployment directory, defaulting to `$(Sts2Dir)/mods/STS2-RitsuLib`. Used by RitsuLib package/build logic to copy RitsuLib into the game's mods directory — **not** this mod's output directory |

## RitsuLib Version Compatibility

> ⚠️ **Important: the manifest key is `min_version`, not `version`**
>
> Each entry in `STS2_Momoi.json`'s `dependencies[]` is `{"id": "STS2-RitsuLib", "min_version": "0.6.7"}`. The game's `ModDependency` (`Core/Modding/ModDependency.cs:10`) only maps `[JsonPropertyName("min_version")]`; writing `version` raises no error but is silently ignored as an unknown member — i.e. no floor at all.
>
> `min_version` is a **hand-picked compatibility floor** and must not drift upward with NuGet: the template's old `SyncManifestDependencies` target rewrote it to whatever package the build resolved (silently raising the floor on every RitsuLib bump, locking out players on older RitsuLib with `MOD_ERROR.DEPENDENCY_VERSION_UNSUPPORTED`). It is now `ValidateManifestDependencies`: **validate only, never rewrite** — missing key errors out, a floor above the compiled package errors out, and the build log prints `STS2-RitsuLib min_version X <= package Y`.
>
> This project's floor of `0.6.7` is empirical: pinning `PackageReference` to `0.6.7` builds the whole project with **0 errors** (same warning count as 0.6.10), so any RitsuLib >= 0.6.7 loads. `min_game_version` still needs manual review. See [Pre-release checklist: dependency floor](#pre-release-checklist-dependency-floor).

### Current version snapshot (as of 2026-05-22)

| Item | Value |
|---|---|
| Current STS2 game version | `0.106.0` |
| Current RitsuLib version | `0.3.0` |
| Template manifest status | `min_game_version` aligned; `dependencies[STS2-RitsuLib].min_version` = `0.6.7` (hand-picked floor, validated but never rewritten by the build) |

### Version mapping

The table summarizes the mainline STS2 target for each boundary RitsuLib release, sourced from the [STS2-RitsuLib Releases](https://github.com/BAKAOLC/STS2-RitsuLib/releases) page. Patch versions not listed follow the range they sit in; check the relevant release notes for boundary versions.

| RitsuLib version | Mainline STS2 target | Compat packages |
|---|---|---|
| `v0.3.0+` (since 2026-05-22) | `0.106.0` | `0.103.2`; `0.104.0` compat removed |
| `v0.2.29` ~ `v0.2.40` | `0.105.1` | `0.104.0`, `0.103.2` |
| `v0.2.27` ~ `v0.2.28` | `0.105.0` | `0.104.0`, `0.103.2` |
| `v0.2.0` ~ `v0.2.26` | `0.104.0` | `0.103.2` (experimental from `v0.2.6`); `0.99.1` compat removed in this range |
| `v0.0.x` / `v0.1.x` | `0.99.1` and earlier | — |

### Package selection: mainline and compat

The template references mainline `STS2.RitsuLib` by default, tracking the latest NuGet version:

```xml
<PackageReference Include="STS2.RitsuLib" Version="*" GeneratePathProperty="true" />
```

**Only enable one RitsuLib package at a time.** If your code still targets an older branch, comment out the mainline and enable the matching compat package:

```xml
<!-- STS2 0.104.0 compatibility branch (no longer maintained since v0.3.0) -->
<PackageReference Include="STS2.RitsuLib.Compat.0.104.0" Version="*" />

<!-- STS2 0.103.2 compatibility branch -->
<PackageReference Include="STS2.RitsuLib.Compat.0.103.2" Version="*" />
```

Compatibility packages only select the matching game branch; they do not restore every old API. Some old mods still need code changes and recompilation.

### Pre-release checklist: dependency floor

> **`PackageReference` in `.csproj` only controls compile-time resolution (`Version="*"` → 0.6.10 today); `dependencies` in `STS2_Momoi.json` is what the loader checks at runtime. They mean different things: package version = what I compiled against; `min_version` = the oldest version I promise still works.**

If the manifest is not synced to the newer RitsuLib version you compile against, players with an old RitsuLib will pass the manifest check and crash at runtime due to missing APIs or signature drift. Conversely, an over-tight manifest will reject players who could otherwise run the mod.

Before every release:

1. The build log must show `STS2-RitsuLib min_version 0.6.7 <= package 0.6.10` (`ValidateManifestDependencies` only validates: a missing `min_version` or one above the compiled package version is a hard build error).
2. To move the floor: temporarily pin `PackageReference` to the target version and build once (only claim it if it compiles with 0 errors), then update `min_version` in `STS2_Momoi.json`, then restore `Version="*"`.
3. When you switch to a compatibility package (`Compat.0.104.0` / `Compat.0.103.2`), also adjust `min_game_version` to the matching branch. Keep `dependencies[].id` as `STS2-RitsuLib` (compatibility packages expose the same mod id to the loader).

### Upgrade notes

#### Upgrading to RitsuLib `v0.3.0` / STS2 `0.106.0`

Major changes (from the [v0.3.0 release notes](https://github.com/BAKAOLC/STS2-RitsuLib/releases/tag/v0.3.0)):

- **Breaking**: `RunSidecar` removed, fully replaced by `RunSavedData`.
- New `TargetType` registration capability for custom `TargetType`s.
- Loader target detection strengthened: branch version files now use hash verification, and mismatched versions are discarded.
- `0.104.0` compatibility removed.

#### Upgrading to RitsuLib `v0.2.27` / STS2 `0.105.0` (historical)

When migrating from an earlier branch (`v0.2.0` ~ `v0.2.26` / STS2 `0.104.0`), check the following:

- Version conditional compilation switched to cumulative interval macros `STS2_AT_LEAST_<ver>`; legacy `STS2_V_<ver>` macros are no longer recommended.
- AnyPlayer / AnyAny targeting logic changed; legacy card targets, base constructor signatures, and registration flows should be checked against the new API.
- Cards support extra icon count labels in the lower-right corner with vanilla UI conflict handling; verify display order and placement for custom UI / icon patches.
- Retain / flush hooks and events have replacements, removals, or `[Obsolete]` markers; migrate legacy uses of `CardRetainedEvent`, `CardsFlushedEvent`, or legacy `Hook.*` entry points.
- `Badge`, `BadgeRuntimeTemplate`, `BadgePool.CreateAll`, and `ModBadgeTemplate` constructor signatures changed; legacy code may need updates to avoid `MissingMethodException`.

## Build

| Command | Behavior |
|---|---|
| `dotnet build .\STS2_Momoi.csproj` | Full build: compile + `CopyMod` + `ExportPCK` |
| `... /p:RunPckExport=false` | Skip PCK export (no `GodotExe` needed) |
| `... /p:CopyModOnBuild=false` | Skip copying to the game's mods directory (output stays in `bin/`) |
| `... /p:RunPckExport=false /p:CopyModOnBuild=false` | C# compile validation only |

A full build runs two MSBuild targets after `Build`:

- **`CopyMod`**: copies the DLL and manifest to the game's `mods/STS2_Momoi` directory.
- **`ExportPCK`**: calls `GodotExe` and exports the PCK to the same mod directory.

> `RitsuLibDeployDir` only controls where the RitsuLib framework itself is deployed locally. This mod's DLL, manifest, and PCK are controlled by `ModOutputDir` (default `$(Sts2Dir)/mods/$(MSBuildProjectName)`).

## Directory Layout

```text
STS2_Momoi/
├── STS2_MomoiCode/   # C# source
├── STS2_Momoi/       # Godot resources, localization, and placeholder scenes
├── STS2_Momoi.csproj
├── STS2_Momoi.json   # Mod manifest
├── project.godot
└── local.props.template
```

`res://STS2_Momoi/...` is the Godot/PCK resource path, mapping to the repository resource directory `STS2_Momoi/`, **not** to the C# namespace. When you create a project from the NuGet template, these directory names, file names, and namespaces are renamed consistently to match the new mod name.

## Template Contents

### Sample character

| Property | Value |
|---|---|
| Type | `STS2_MomoiCharacter` |
| Expected ID | `STS2_MOMOI_CHARACTER_STS2_MOMOI_CHARACTER` |
| Starter deck | 4 × `STS2_MomoiStrike`, 4 × `STS2_MomoiDefend`, 1 × `STS2_MomoiRelic` |
| Assets | Configured via `CharacterAssetProfile`. The template only specifies static placeholder assets; unspecified audio, trail, transition, etc. fall back through `PlaceholderCharacterId` |

### Sample cards and relic

| Type | Pool | Expected ID |
|---|---|---|
| `STS2_MomoiStrike` (attack) | character card pool | `STS2_MOMOI_CARD_STS2_MOMOI_STRIKE` |
| `STS2_MomoiDefend` (skill) | character card pool | `STS2_MOMOI_CARD_STS2_MOMOI_DEFEND` |
| `STS2_MomoiRelic` | `STS2_MomoiRelicPool` | `STS2_MOMOI_RELIC_STS2_MOMOI_RELIC` |

### Static placeholder assets

**Images** (`res://STS2_Momoi/images/...`):

- `cards/STS2_MomoiStrike.png`, `cards/STS2_MomoiDefend.png`: sample card art.
- `relics/STS2_MomoiRelic.png`: sample relic icon.
- `characters/STS2_Momoi_character_*.png`: character icons, select art, map marker, and energy icons.

**Scenes** (`res://STS2_Momoi/scenes/characters/...`):

| Scene | Purpose | Placeholder structure |
|---|---|---|
| `STS2_Momoi_character.tscn` | Combat character | `%Visuals`, `%Bounds`, `%IntentPos`, `%CenterPos`, `%TalkPos` |
| `STS2_Momoi_energy_counter.tscn` | Energy counter | `%EnergyVfxBack`, `%Layers`, `%RotationLayers`, `%EnergyVfxFront`, `Label` |
| `STS2_Momoi_merchant.tscn` | Merchant | — |
| `STS2_Momoi_rest_site.tscn` | Rest site | `%ControlRoot`, `%SelectionReticle`, `%Hitbox`, `%ThoughtBubbleRight`, `%ThoughtBubbleLeft` |
| `STS2_Momoi_character_select_bg.tscn` | Character select background | — |

These resources only exist to make the template visible and replaceable; they do not try to reproduce vanilla animation quality. After copying the template, replace them with your own assets. If you change paths, update the corresponding `AssetProfile` fields.

## Manifest Format

`STS2_Momoi.json` is the mod manifest. The game loader reads it at startup to identify the mod, check dependencies, and decide whether to load. Full example:

```json
{
  "id": "STS2_Momoi",
  "name": "STS2_Momoi",
  "pck_name": "STS2_Momoi",
  "author": "Author",
  "description": "A starter Slay the Spire 2 mod template built on RitsuLib.",
  "version": "0.0.0",
  "has_pck": true,
  "has_dll": true,
  "affects_gameplay": true,
  "min_game_version": "0.106.0",
  "dependencies": [
    { "id": "STS2-RitsuLib", "version": "0.3.0" }
  ]
}
```

### Field reference

| Field | Type | Description |
|---|---|---|
| `id` | string | Unique mod identifier. **Must match `Entry.ModId` exactly**, and should also match the `mods/<id>` directory name. In-game dependency lookups, localization key prefixes, and resource paths all depend on this value |
| `name` | string | Display name shown in the mod list. May contain spaces and non-ASCII characters |
| `pck_name` | string | `.pck` file name (without extension). **Must match the actual PCK file produced by `.csproj`**, or resources will not load even with `has_pck=true` |
| `author` | string | Display-only author name |
| `description` | string | Short description shown in the mod list |
| `version` | string | Version of this mod itself. SemVer (`MAJOR.MINOR.PATCH`) is recommended. Bump on every release |
| `has_pck` | bool | Whether the mod ships a `.pck`. Code-only mods can set `false` and skip `ExportPCK` |
| `has_dll` | bool | Whether the mod ships a `.dll`. Resource-only mods can set `false` |
| `affects_gameplay` | bool | Whether the mod affects gameplay. When enabled, the game flags saves/achievements/etc.; only purely cosmetic / localization mods should set this to `false` |
| `min_game_version` | string | Minimum compatible STS2 version. Older games refuse to load. **Must align with the game branch targeted by the RitsuLib package selected in `.csproj`** (see [RitsuLib Version Compatibility](#ritsulib-version-compatibility) above) |
| `dependencies` | array | Dependency list. Each entry uses `id` + `min_version`. Old plain-string arrays still load (the game migrates them and logs `MIGRATION_REQUIRED`), but use object form |
| `dependencies[].id` | string | The depended-on mod's `id`. RitsuLib itself uses `STS2-RitsuLib` |
| `dependencies[].min_version` | string | **Minimum** version of the dependency (semver, e.g. `0.6.7`). Spelling it `version` gets silently ignored, i.e. no version check at all. The loader compares it against the dependency's own manifest `version`; below the floor → `MOD_ERROR.DEPENDENCY_VERSION_UNSUPPORTED` and this mod fails to load |

## Development Tips

- Prefer `AssetProfile` for new content; only override legacy `Custom...Path` fields for individual compatibility cases.
- If a character resource field is not specified, RitsuLib fills it from the vanilla character config referenced by `PlaceholderCharacterId`.
- Resource paths must start with `res://`; verify the directory name and casing inside the PCK are correct.
- For `.tscn` files, make sure the scene is packed into the mod resources. If it needs a script, prefer a local wrapper class and call `EnsureGodotScriptsRegistered(...)` from `Entry.Initialize()`.
