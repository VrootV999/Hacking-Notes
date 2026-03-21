Guide to Hack Unity Android Games

# Startup Flow
```md
- com.unity3d.player.UnityPlayerActivity(triggers UnityPlayer)
- com.unity3d.player.UnityPlayer(loads all the libraries)
- libunity.so, libmain.so, libil2cpp.so(if present)
- IL2CPP runtime(Intermediate Language(C#)to cpp)
- global-metadata.dat
- game assembles(assembly-Csharp)
```

# Game loading
### Stored as C# assembly(Mono)
- PC: GameName_Data/Managed/
- Android: assets/bin/Data/Managed/Assembly-Csharp.dll
- Use Ilspy dnSpyEx dotpeek
```md
- files
Assembly-CSharp.dll
Assembly-CSharp-firstpass.dll
UnityEngine.dll
mscorlib.dll

- runtime
Unity runtime
    ↓
Mono runtime
    ↓
Load managed assemblies
    ↓
Assembly-CSharp.dll
    ↓
JIT compile methods
    ↓
Execute game scripts
```

### IL2CPP backend
- The game logic is compiled into `libil2cpp.so` and the classes and metadata is stored in `global-metadata.dat`
- At GameAssembly.dll or libil2cpp.so 
- metadata at global-metadata.dat
- Use Il2cppDumper Il2cppInspector Ghidra Ida binary ninja
```md 
- buildtime
C# scripts
     ↓
Unity IL
     ↓
IL2CPP converts IL → C++
     ↓
C++ compiled with clang
     ↓
libil2cpp.so

- runtime
Unity Runtime
     ↓
libil2cpp.so loaded
     ↓
global-metadata.dat loaded
     ↓
IL2CPP reconstructs classes
     ↓
methods mapped to native functions
     ↓
execute game logic
```


mscorlib.dll-resources.dat System.Data.dll-resources.dat System.Drawing.dll-resources.dat i got this in /assets/bin/Data/Managed/Resources(it is the extraction from apktool) then i got this boot.config data.unity3d Managed resources.resource RuntimeInitializeOnLoads.json ScriptingAssemblies.json sharedassets1.resource unity_app_guid 'unity default resources' in my /assets/bin/Data but also the global-metadata.dat at the /assets/bin/Data/Managed/Metadata part


| File / Folder                                                                   | Purpose                                       | Indicates Build                                                        |
| ------------------------------------------------------------------------------- | --------------------------------------------- | ---------------------------------------------------------------------- |
| `/assets/bin/Data/Managed/Assembly-CSharp.dll`                                  | Main game C# code                             | **Mono**                                                               |
| `/assets/bin/Data/Managed/Assembly-CSharp-firstpass.dll`                        | Optional precompiled scripts                  | **Mono**                                                               |
| `/assets/bin/Data/Managed/UnityEngine.dll`                                      | Engine C# code                                | **Mono**                                                               |
| `/assets/bin/Data/Managed/mscorlib.dll`                                         | .NET core library                             | **Mono**                                                               |
| `/assets/bin/Data/Managed/Resources/*.dll-resources.dat`                        | Localization / resource strings               | Mono or IL2CPP (not code)                                              |
| `/assets/bin/Data/Managed/Metadata/global-metadata.dat`                         | Metadata for reflection / serialization       | **Mono** (if no `libil2cpp.so`), **IL2CPP** (if `libil2cpp.so` exists) |
| `libil2cpp.so` (in `/lib/`)                                                     | Native compiled game code                     | **IL2CPP**                                                             |
| `/assets/bin/Data/data.unity3d`, `sharedassets*.resource`, `resources.resource` | Game assets (textures, audio, prefabs)        | Both Mono & IL2CPP                                                     |
| `boot.config`                                                                   | Unity engine startup config                   | Both Mono & IL2CPP                                                     |
| `RuntimeInitializeOnLoads.json`, `ScriptingAssemblies.json`                     | Lists scripts / assemblies to load at runtime | Both Mono & IL2CPP                                                     |

### Asset Extraction
- .assets : Textures, audio, meshes, shaders
- .sharedAssets: shared assets across scenes
- .resource/.resS: Large binary data(textures/audio)
- .bundle/AssetBundles: Downloadable asset packs
- .unity3d: Older bundle format
- .split0/.split1 : split asset files for mobile devices

- Located at GameName_data/ in PC
- Located at assets/bin/Data in android 
- Tools to use are AssetRipper AssetStudio UABEA
---
