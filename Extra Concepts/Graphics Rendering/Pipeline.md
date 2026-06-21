# Graphics Pipeline

## Input Assembler(IA)

> [!NOTE]
> A vertex buffer which contains vertex attribute to each triangle that makes up a 3d model

- We provide it to a Input Assembler chunks of Vertex which has stuff like Position, UV coordinates and some Normals in general and then the components of each (like how many positions,UV coordinates and normal is provided cuz it can 2D or 3D for positions or use polar components for Normal to pack it into two components)
- this is typically structured as an array of structs. Each vertex contains 8 floats in total
- Position (X,Y,Z) (3floats/12B): `Defines where a Vertex sits in a 3d space`
- UV (U,V)(2floats/8B): `Defines how a 2D texture maps onto the 3d surface`
- Normals ($N\subset{x},N\subset{y},N\subset{z}$)(3floats,12B): `Defines the direction the vertex is facing which is critical for calculating lighting`
- 4Bytes each or 32 bits each
- The input assembler also provides a vertex ID which starts at 0
- The ID takes up one component and get stored as uint16
- Every row is a vertex
- Every single vertex in the buffer will be passed to veVertex Shader's job is to manipulate individual points,rtex shader

```rust
struct Vertex {
    position: (f32,f32,f32?)
    uv: (f32,f32)
    normal: (f32,f32)
}

//dumbass gemini's IDEA of a input vertex
#[repr(C)] // Guarantees C-style memory layout (no field shuffling)
#[derive(Copy, Clone, Debug)]
pub struct Vertex {
    pub position: [f32; 3], // 3D Position: X, Y, Z
    pub uv: [f32; 2],       // 2D Texture Coordinates: U, V
    pub normal: [f32; 3],   // 3D Normal Vector: Nx, Ny, Nz
}
```
In summary 
1. Pulls raw bytes from GPU memory buffer(verticies and indexes)
2. Converts data type on the fly(unpacking compressed colors or auto-padding 2D vectors to 4D vectors)
3. Groups verticies into geometric primitives based on your instructions
4. You Provide `4 inputs` 
    1. Vertex Buffer(Positions, UV, Normals, Colors)
    2. Index Buffer (An array of integer index which acts like a lookup table) (eliminates duplicate vertex processing)
    3. Input Layout (A blueprint for IA which tells how to interpret raw bytes in the vertex buffer)(has three metrics)
        - Stride: The total byte-size of a single vertex (tells the IA how far to jump to reach the next one).
        - Offset: The starting byte position of a specific attribute within that vertex chunk.
        - Format: The data type (e.g., three 32-bit floats, four 8-bit integers, etc.).
    4. Primitive Topology (This tells the IA how to group the incoming vertices. The most common topologies include)
        - Point List: Every vertex is an isolated point.
        - Line List / Strip: Vertices form independent lines, or continuous connect-the-dots lines.
        - Triangle List: Every 3 vertices form an independent triangle.
        - Triangle Strip: Every new vertex forms a triangle with the last two vertices (saves memory bandwidth).
        - Patch List: Used for Tessellation shaders (defines control points rather than hard geometry).
5. `Advanced Features Built Into the Hardware`
    -To ensure nothing is forgotten, the IA also handles complex pipeline behaviors automatically:
6. `Instancing (Data Step Rate)`
    - The IA allows you to draw the same 3D mesh thousands of times with a single draw call (e.g., a forest of trees or a crowd of characters). To do this, you configure the IA's Input Slot Class/Step Rate:
        - `Per-Vertex Data`: Move to the next data slot for every vertex (e.g., unique model shapes).
        - `Per-Instance Data`: Move to the next data slot only after drawing a whole instance of the object (e.g., unique world-positions or colors for each individual tree).
7. `Type conversion & Normalisation`
    - If your buffer stores colors as 4 bytes (RGBA, 0-255) to save memory, but your shader needs them as floats (0.0-1.0), the IA automatically performs this hardware-level division by 255.5 before sending it to the vertex shader.
8. `Built-in System Values (Generators)`
    - The IA injects unique ID tags directly into your Vertex Shader inputs without you needing to put them in your vertex buffers:
        - VertexID (or gl_VertexIndex): The sequential counter of the current vertex.
        - InstanceID (or gl_InstanceIndex): The counter tracking which copy of the mesh is currently rendering.
```
[Raw Bytes] + [Index Table] ---> ( INPUT ASSEMBLER ) ---> [Triangles / Lines] ---> [Vertex Shader]
                                  ^  Uses Layout & Topology
```

### Steps
`Step 1`: Read the Draw Command — The IA receives the execution command from the CPU, determining whether it is running a standard draw call or an indexed/instanced draw call.

`Step 2`: Resolve Indices (If Indexed) — If an index buffer is bound, the IA looks up the current index values to determine exactly which vertices from the vertex buffer need to be fetched, skipping duplicate vertices.

`Step 3`: Calculate Memory Addresses — Using the configured Stride (byte size of one vertex), the IA calculates the exact memory offsets in VRAM to find the raw binary data for each requested vertex attribute.

`Step 4`: Fetch and Unpack Raw Bytes — The IA pulls the raw data from the vertex buffer streams.

`Step 5`: Apply Type Conversions and Padding — The hardware automatically converts data types if needed (e.g., normalizing 8-bit integers into 0.0–1.0 floats) and auto-pads missing vector data (e.g., filling a 2D position out to 4D by automatically injecting Z=0.0 and W=1.0).

`Step 6`: Inject System-Generated Values — The IA automatically generates and attaches built-in hardware counters, such as the current VertexID and InstanceID, to the data stream.

`Step 7`: Group into Geometric Primitives — Following the specified Primitive Topology (e.g., Triangle List, Line Strip), the IA groups the gathered vertices into discrete geometric shapes.

`Step 8`: Stream to the Vertex Shader — The fully assembled, cleanly structured primitives are pushed directly into the execution pipelines of the Vertex Shader stage.

---
## Vertex Shader
- Takes in all the attributes of a single vertex and outputs a new set of attributes. 
- It will use external data like a matrix. 
- It multiples the position with the matrix to transform the position. 
- It comes out as a vector which is transoformed by the matrix
- Every time each value should be in the position between -1 and +1
- Every vertex that ends after this process will end up in a cube of 2x2x2

Vertex Shader is primarily responsible for transforming geometry from its raw 3D file format state into a format that can actually be projected onto a 2D screen, alongside preparing structural data for lighting.

###  `Coordinate Space Transformation(MVP)`
A 3D model has its vertices are relative to the center of that model (Local/Model Space). The Vertex Shader must transition this position through a sequence of spaces using matrix multiplications:
- Model to World: Positions the object inside your 3D game world.

- World to View (Camera): Shifts the entire world relative to where the camera is looking.
- View to Clip (Projection): Distorts the 3D space into a 2D frustum (accounting for field-of-view and perspective compression).
$V_{clips} = M_{Projection} x M_{View} x M_{World} x V_{Local_10}$
###  `Vertex Animation and Displacement`
Because the Vertex Shader can manipulate positions before anything is drawn, it is the home of procedural mesh manipulation.
- Skeletal Animation (Skinning): For characters, the vertex shader blends multiple bone matrices together to bend the mesh around an animated skeleton.
- Displacement Mapping: It can read a texture (like a heightmap) and physically push vertices upward to create realistic terrain, water waves, or cloth ripples.

###  `Transforming Normal Vectors`
- Normals (the orientation vectors you mentioned earlier) cannot just be multiplied by the standard World matrix because if an object is scaled unevenly, the normals will skew and break your lighting.
- The Vertex Shader calculates a special Inverse-Transpose World Matrix to safely rotate and scale the normals into World Space so that lighting math behaves correctly later in the pixel shader.

###  `Generating Interpolants for the Pixel Shader`
- The Vertex Shader sets up the variables that the rasterizer will blend across the surface of a triangle. For example, it passes through UV coordinates and calculates world-space positions. If Vertex A has a UV of 0.0 and Vertex B has a UV of 1.0, the pipeline will interpolate those values smoothly for every pixel in between.

###  `Execute Contraints(It can't do these)`
 To achieve blistering parallel speeds, the GPU isolates each vertex execution.
- Complete Isolation: A vertex shader processing Vertex #45 has absolutely zero knowledge of Vertex #44 or Vertex #46.
- Topology Ignorance: It does not know what triangle it belongs to, nor does it know if it's being drawn as a line, a point, or a polygon. It treats every vertex as an isolated point in space.

### `Inputs vs. Outputs`
**Inputs**
- Per-Vertex Attributes: Positions, UVs, Normals, Tangents, and Color streams (assembled by the IA).
- Constant Buffers / Uniforms: Global data shared across the entire draw call, such as the Model-View-Projection (MVP) matrices, time variables, or animation bone arrays.

**Outputs**
- clip_position (SV_Position / gl_Position): This is mandatory. The vertex's final coordinate in 4D Homogeneous Clip Space. The GPU requires this to know where to draw the vertex on your monitor.
- User-Defined Outputs: Transformed world positions, texture coordinates, calculated vertex colors, or TBN matrices for normal mapping.

### Steps
`Step 1`: Fetch Input Data — The shader receives its dedicated vertex attributes from the Input Assembler alongside global matrix data from uniform buffers.

`Step 2`: Apply Vertex Animation — If applicable, the shader modifies the raw local position using skeletal bone weights or procedural math (e.g., wind or wave equations).

`Step 3`: Transform Position to Clip Space — The position vector is multiplied by the combined Model, View, and Projection matrices to determine its position relative to the screen.

`Step 4`: Transform Surface Vectors — Normal and tangent vectors are multiplied by the inverse-transpose matrix to bring them into world/view space without distortion.

`Step 5`: Prepare Custom Varyings — Texture coordinates (UVs) and world positions are mapped onto output registers.

`Step 6`: Handover to Hull Shader - Send it to hull shader

---
## Hull shaders

- The Hull Shader’s job is to look at a group of points—called a Patch—and decide how heavily the GPU should subdivide that patch into finer geometry. This allows engines to dynamically add millions of polygons to a model on the fly based on how close it is to the camera.

- Instead of rendering triangles directly, the Input Assembler feeds the pipeline primitive "Patches". The Vertex Shader processes these control points, and then hands them to the Hull Shader.

### `The Dual-Phase Architecture` 
- The Hull Shader is unique because it actually executes your code in two completely distinct, parallel phases for every patch.
Phase A: The Control Point Phase(Per-Control Point)
    This phase runs in parallel for every output control point you want to generate.
    - `The Logic`: It reads the control points coming from the Vertex Shader and outputs a new set of control points.
    - `The Transformation`: Often, this is just a "pass-through" phase where it copies the vertex data straight through. However, it can also transform the math basis—for example, taking 4 linear points and converting them into a smooth Bézier patch curve.
Phase B: The Patch Constant Phase (Per-Patch)
    This phase runs exactly once per entire patch, regardless of how many control points it has. This is where the real magic happens.
    - `The Logic`: It calculates global data for the patch.
    - `The Tessellation Factors`: Its primary job is to output Tessellation Factors (Edge factors and Inside factors). These numbers tell the hardware exactly how many pieces to chop the patch into.

### `What It can do`
- It Can Discard Geometry: If a patch is completely behind the camera (frustum culled), the Hull Shader can set the tessellation factor to 0. The GPU will immediately drop the entire patch, skipping all further work.
- It Cannot Create New Vertices Yet: The Hull Shader only sets up the instructions and data. It doesn't actually create the new triangles itself; it passes its calculations to the fixed-function Tessellator hardware block, which physically cuts up the geometry.

### Inputs vs. Outputs
- Inputs
    - Input Patch: A collection of control points processed by the Vertex Shader.
    - Patch ID: A built-in counter tracking which specific patch is being processed.
- Outputs
    - Output Control Points: The geometry basis passed forward to the final Tessellation stage (Domain Shader).
    - Tessellation Factors: * Edge Factors: How much to subdivide the outer borders of the patch (crucial for stitching adjacent patches together without gaps).
        - Inside Factors: How much to subdivide the interior surface of the patch.

### Steps
`Step 1`: Receive Input Patch — The shader takes in the array of control points that were pre-processed by the Vertex Shader.

`Step 2`: Run Control Point Phase — The GPU spawns parallel threads to process and format each individual output control point required for the patch surface definition.

`Step 3`: Run Patch Constant Phase — A separate execution group evaluates the patch as a single entity to calculate world space properties.

`Step 4`: Calculate Tessellation Factors — Based on custom logic (like camera distance, screen-space size, or performance budgets), the shader computes how finely the edges and interior of the patch should be subdivided.

`Step 5`: Perform Frustum Culling — If the patch constants determine the geometry is off-screen, it sets the factors to zero to instantly kill the primitives.

`Step 6`: Handover to Hardware Tessellator — The shader outputs the final control points and the tessellation factors, signaling the fixed-function hardware to begin physically dividing the patch into thousands of tiny triangles.

---
## Tessellator

### Core Philosophy
- The Tessellator is completely blind to your actual 3D world. It doesn't know where your camera is, it doesn't know what a 3D model looks like, and it doesn't know anything about lighting or coordinates.
- Instead, it works entirely in an Abstract Domain (a flat, normalized 2D space ranging from 0.0 to 1.0). Depending on what you configured in your pipeline, it works on one of three shapes:
    - Isoline: A simple 1D line segment.
    - Triangle: A flat, 2D barycentric triangle.
    - Quad: A flat, 2D square.


### What it actually Does
- The Tessellator takes two inputs: the chosen Abstract Domain Type and the Tessellation Factors calculated by your Hull Shader.It then executes three specific actions:
    1. Edge and Interior Subdivision
        It reads the Edge and Inside factors. If the Hull Shader requested an inside tessellation factor of 4, the Tessellator will mathematically slice up the interior of that abstract 0.0…1.0 quad or triangle into a grid-like pattern.
    2. Index Generating
        As it chops up the domain, it dynamically creates a massive web of brand-new vertices. Because these vertices will form triangles, the Tessellator automatically hooks them together, generating the layout indices required to turn these points into actual topology (like a triangle list).
    3. Outputting Coordinate Locations
        For every single brand-new vertex it creates, it outputs a coordinate representing where that vertex sits inside the flat abstract space:
        - For a Quad, it outputs a 2D Cartesian coordinate: (u,v)
        - For a Triangle, it outputs a 3D Barycentric coordinate: (x,y,z) (where x+y+z=1.0)

### The structural rule
- Because it is a fixed-function hardware block, it has rigid limitations built into the GPU architecture:

- Max Limit: The maximum tessellation factor is capped by hardware at 64.0 (in modern graphics APIs like DirectX 12 and Vulkan). If your Hull Shader requests a factor of 128.0, the Tessellator clamps it to 64.0.

- Zero Discard: If any edge factor is calculated as 0.0 or less, the Tessellator skips processing the primitive entirely, effectively killing it.

- Fractional Tessellation: It can handle non-integer factors (like 4.5). Instead of making a vertex jump into existence violently as the camera moves closer, it uses specialized algorithms to smoothly "fade" or grow new triangles from the edges of old ones, preventing distracting geometric popping artifacts.

### Summary
- Step 1: Read Configuration and Factors — The hardware initializes its state based on the abstract domain shape (Isoline, Triangle, Quad) and grabs the Tessellation Factors output by the Hull Shader.

- Step 2: Subdivide Edges — The hardware breaks the outer boundaries of the abstract 0.0…1.0 domain into segments according to the specific edge factors to ensure seamless connections with neighboring patches.

- Step 3: Subdivide Interior — The hardware cuts up the inner surface area of the abstract domain based on the interior tessellation factors, forming a dense grid.

- Step 4: Generate Domain Coordinates — The block calculates precise fractional coordinates ((u,v) or barycentric values) mapping where each newly created vertex lies within that generic flat space.

- Step 5: Stitch Topology Indices — The hardware automatically generates the index streams required to legally bind these new vertices into valid triangles.

- Step 6: Stream to the Domain Shader — The Tessellator outputs a massive wave of raw abstract coordinates and topological connections, passing them directly to the Domain Shader stage where they will finally be mapped back into your real 3D scene.

---
## Domain Shader
### Core Responsibilities

The Domain Shader is the second programmable stage in the Tessellation pipeline. It acts as the "creator of reality" for the new geometry. Its core responsibility is to take the blind, flat mathematical decisions made by the Tessellator and map them into the actual 3D virtual world.

#### A. Position Reconstruction via Interpolation

- The Tessellator gives the Domain Shader an abstract location (like $(u, v) = (0.5, 0.5)$), and the Hull Shader hands it the original 3D control points. The Domain Shader must manually blend these together using interpolation math to determine where that new coordinate actually lies on the 3D surface.

* **For Quads:** It uses Bilinear Interpolation (LERP) across the 4 corners of the patch.
* **For Triangles:** It uses Barycentric Interpolation to blend across the 3 points of the triangle.
* **For Curved Surfaces:** It calculates complex parametric polynomial curves (like Bézier patches) to make the geometry mathematically smooth.

#### B. Displacement Mapping (Applying Micro-Geometry)

- This is the ultimate purpose of Tessellation. Now that the Domain Shader has calculated a dense grid of 3D positions, it can sample a **Heightmap / Displacement Texture**.

* It reads the texture at the vertex's UV coordinate.
* It scales that value by a displacement factor.
* It physically offsets the vertex position along its 3D Normal vector.
This transforms flat geometry into real, physical micro-details like jagged rocks, brick crevices, or ocean waves that can catch shadows and block the camera view.

#### C. Final Coordinate Space Transformation

Just like a Vertex Shader, the Domain Shader holds the final responsibility for positioning. Once the displaced 3D world position is calculated, the shader must multiply it by the **View-Projection Matrix** to transform it into 4D Homogeneous Clip Space.


### 2. Execution Constraints (What it *Cannot* Do)

* **Isolated Execution:** The Domain Shader runs concurrently across the GPU for **every single individual coordinate** output by the Tessellator. A thread processing coordinate A knows absolutely nothing about coordinate B.
*  **Topology Ignorance:** It doesn't know *how* the vertices are connected to form triangles; it only knows its own specific location in the abstract domain and the overall patch data.

### 3 Inputs vs Outputs
#### Inputs

- **The Abstract Domain Coordinates:** The $(u,v)$ or barycentric coordinates output by the Tessellator hardware block.
- **The Output Control Points:** The structural 3D points passed forward from the Hull Shader phase.
- **The Patch Constant Data:** Global patch variables (like edge/inside factors or custom values calculated by the Hull Shader).
- **Global Textures/Uniforms:** The heightmaps, displacement textures, and View-Projection matrices.

#### Outputs

* **`clip_position` (`SV_Position` / `gl_Position`):** **Mandatory.** The final position of the newly created vertex on the screen.
* **Varyings for the Pixel Shader:** Fully interpolated UV coordinates, world-space positions, and transformed normal vectors ready for lighting calculations.

### Summary of Steps (The Sequential Checklist)

When an abstract coordinate leaves the Tessellator, the Domain Shader processes it through these precise stages:

* **Step 1: Fetch Abstract Coordinates and Patch Control Points** — The shader initializes by grabbing the flat mathematical coordinate from the Tessellator and the corresponding 3D control point array from the Hull Shader.
* **Step 2: Interpolate the Base 3D Position** — Using the abstract location, the shader executes interpolation math (linear or parametric) to find the base 3D coordinate on the patch surface.
* **Step 3: Interpolate Surface Attributes** — The shader mathematically blends texture coordinates (UVs) and vertex normal vectors across the surface for this specific location.
* **Step 4: Sample the Displacement Map** — The shader uses the interpolated UV coordinates to sample a texture heightmap from VRAM.
* **Step 5: Displace the Vertex** — The shader physically shifts the 3D position vector outward or inward along the calculated normal vector based on the heightmap value.
* **Step 6: Transform to Clip Space** — The newly detailed 3D position is multiplied by the View-Projection matrix to compute its final position on the display grid.
* **Step 7: Stream to the Next Pipeline Phase** — The shader outputs the mandatory `clip_position` along with custom varyings, exiting the Tessellation stage and handing the geometry off to the Geometry Shader or Rasterizer.

---
## Geometry Shader(GS)
This is the final, entirely optional programmable shader stage before the geometry is flattened into pixels. While all previous stages can only manipulate data that *already exists*, the Geometry Shader is unique because it has the power to **destroy geometry or break the laws of conservation and create brand new geometry** on the fly.

### 1. Core Responsibilities (What Happens in Detail)

The Geometry Shader is the only stage in the pipeline that has a full, macro-view of an entire geometric primitive. It doesn't look at isolated vertices; it processes whole triangles, lines, or points at the same time.

#### A. Dynamic Primitive Alteration (Creation & Destruction)

The Geometry Shader takes an entire primitive as an input and can output zero, one, or *many* primitives.

* **Destruction (Culling):** It can choose to output absolutely nothing. If a triangle fails a specific game-logic test, the GS drops it, deleting it from the pipeline entirely.
* **Creation (Amplification):** It can take a single point in space and explode it into a flat camera-facing quad (Billboarding), or take a single triangle and subdivide it into a spiky cone.

#### B. Common Use Cases

Because of its ability to spawn geometry out of thin air, developers historically used the GS for:

* **Billboarding / Particle Systems:** Passing a single vertex point to the GPU, and letting the GS expand that point into a 4-vertex quad to render smoke, sparks, or leaves.
* **Wireframe Rendering:** Calculating the distance from a pixel to the edges of its triangle to cleanly draw outline wireframes over a mesh.
* **Fur / Hair Generation (Fin Extrusion):** Generating tiny extruded geometric "fins" along the sharp edges of a 3D model to simulate fuzzy lighting or grass.

#### C. Layered Rendering (Cube Mapping)

The Geometry Shader can duplicate incoming geometry and send different copies to different layers of a render target simultaneously. This is highly useful for generating a **Real-time Cube Map** (for reflections) or shadow maps in a single pass, rather than rendering the entire scene 6 separate times from scratch.

### 2. Execution Constraints (The Massive Catch)

While the Geometry Shader sounds incredibly powerful, it comes with a major performance warning in modern graphics development:

* **The Amplification Bottleneck:** You must declare the maximum number of vertices the GS can output upfront. The GPU must allocate memory rings on the silicon to hold this potential data. If your GS has a high output limit, it drastically chokes the GPU's parallel processing capabilities.
* **The Performance Penalty:** On modern hardware, the Geometry Shader is notoriously slow for heavy mesh modifications. (In modern tech like DirectX 12 or Vulkan, it is largely replaced by **Mesh Shaders** for this reason).

### 3. Inputs vs. Outputs

#### Inputs

* **Full Primitives:** Instead of a single vertex, it takes an array of vertices representing the structure:
* `Point`: Array of 1 vertex.
* `Line`: Array of 2 vertices.
* `Triangle`: Array of 3 vertices.
* *Adjacency variations*: Can take up to 6 vertices to see neighboring triangles!

#### Outputs

* **Primitive Streams:** The GS pushes vertices sequentially into an output stream topology (e.g., a `TriangleStream` or `PointStream`). Once it pushes enough vertices to satisfy the topology, a new primitive is born.


### Summary of Steps (The Sequential Checklist)

When a primitive leaves the previous stage, the Geometry Shader processes it through these precise steps:

* **Step 1: Receive Complete Primitive Array** — The shader initializes by gathering the entire group of vertices that form a distinct geometric shape (e.g., all 3 vertices of a triangle).
* **Step 2: Read Global / Adjacency Information** — The shader evaluates the overall geometry, including any optional neighbor-vertex data, to understand the surrounding structural context.
* **Step 3: Execute Custom Geometric Logic** — The shader runs its user-defined code to calculate modifications (e.g., calculating face normals or measuring edge lengths).
* **Step 4: Execute Creation/Destruction Loops** — The program enters a loop where it decides whether to discard the shape, pass it through untouched, or calculate brand-new vertex properties.
* **Step 5: Transform New Vertices to Clip Space** — For every vertex the shader decides to create, it must compute its custom attributes and multiply its position by the View-Projection matrix to establish its `clip_position`.
* **Step 6: Append Vertices to the Output Stream** — The shader uses explicit commands (like `OutputStream.Append()`) to emit the formatted vertices sequentially.
* **Step 7: Restart Primitive Strip (Optional)** — If generating disconnected shapes, the shader invokes a primitive cut command (like `RestartStrip()`) to signal the completion of one shape and the start of another.
* **Step 8: Flush Stream to Rasterizer** — The shader finishes execution, pushing the newly minted stream of primitives out to the Stream Output buffer or directly into the Rasterizer stage.

---
## Rasterizer
The Rasterizer is a highly optimized, **fixed-function hardware block**. You cannot write a shader for it. Its core responsibility is to act as the bridge between the mathematical world of continuous 3D vector geometry (triangles, lines, points) and the discrete 2D grid world of your monitor's screen pixels.

### 1. Core Responsibilities (What Happens in Detail)

The Rasterizer takes the primitives that survived clipping and projects them onto the 2D pixel grid, determining exactly which screen pixels are covered by the geometry.

#### A. Clipping and Homogeneous Divide (The 3D to 2D Flattening)

Before determining pixels, the Rasterizer ensures the geometry is legally visible on screen:

1. **Clipping:** It compares the geometry against the borders of the viewing screen area (the frustum). Any triangles partially off-screen are sliced, and the parts outside are thrown away.
2. **Homogeneous Divide:** It divides the $X, Y, Z$ components of the position by the $W$ component ($X/W, Y/W, Z/W$). This process, known as perspective division, physically shrinks objects that are far away, creating the illusion of 3D depth on a flat screen.

#### B. Face Culling (Skipping Hidden Geometry)

To avoid wasting processing power, the Rasterizer calculates the winding order of the triangle vertices (whether they connect clockwise or counter-clockwise from the camera's perspective). If a triangle is facing away from the camera (like the back wall of a closed house), the Rasterizer **culls** (deletes) it instantly.

#### C. Pixel Coverage Testing (Scan Conversion)

The hardware loops through a 2D viewport grid and checks which pixel centers fall inside the boundaries of the triangle. For every pixel center wrapped by the triangle, the Rasterizer spawns a **Fragment** (a potential pixel).

#### D. Attribute Interpolation (The Perspective-Correct Blend)

This is a massive job. The Vertex or Domain shader outputs values attached only to the *corners* of the triangle (like UVs, Normals, or Colors). The Rasterizer takes those corner values and mathematically blends them across the surface using perspective-correct interpolation. If Vertex A has a UV of 0.0 and Vertex B has a UV of 1.0, a fragment generated exactly in the middle will be assigned a UV of 0.5.

### 2. Execution Constraints (What it *Cannot* Do)

* **No Programmable Logic:** You cannot inject custom loops or conditional code here. You can only tweak its behavior by configuring the pipeline state (e.g., toggling wireframe mode vs. solid mode, or changing the culling direction).
* **No Final Color Allocation:** The Rasterizer does not decide the color of the pixel. It only flags *where* fragments exist and sets up the math data for the Pixel/Fragment Shader to calculate the final color later.

### 3. Inputs vs. Outputs

#### Inputs

* **Primitives in Clip Space:** The mathematically transformed vertices and topology streams coming from the final geometric stage.
* **Viewport Configuration:** State settings defining the width, height, and depth limits of the target rendering window.

#### Outputs

* **Fragments:** A stream of pixel coordinate spaces accompanied by cleanly interpolated attributes (UVs, world positions, normals) fed directly into parallel instances of the Pixel Shader.

### Summary of Steps (The Sequential Checklist)

When geometric primitives are pushed into the Rasterizer, the hardware processes them through these precise steps:

* **Step 1: Perform Frustum Clipping** — The hardware slices triangles that cross the boundaries of the screen space, discarding vertices that fall outside the viewing volume.
* **Step 2: Execute Perspective Division** — The block divides the geometric vectors by their $W$ scale component, transforming 3D coordinates into Normalized Device Coordinates (NDC).
* **Step 3: Map to Viewport Coordinates** — The normalized coordinates are scaled and mapped directly onto the actual pixel dimensions of your current render target screen.
* **Step 4: Evaluate Backface Culling** — The hardware analyzes the 2D winding order of the vertices to identify back-facing polygons and discards them before calculating pixel coverage.
* **Step 5: Determine Pixel Coverage (Scan Conversion)** — The raster engine tests the boundaries of the screen grid, identifying every individual pixel center that is covered by the geometry.
* **Step 6: Interpolate Fragment Attributes** — The hardware applies perspective-correct mathematical blending across the triangle's surface to calculate unique UVs, normals, and colors for every covered pixel location.
* **Step 7: Spawn and Dispatched Fragments** — The Rasterizer packages these screen positions and interpolated attributes into "Fragments" and dispatches them to the Pixel Shader stage to compute final visibility and color.

---
### Pixel Shader
This is a highly **programmable** stage and is the absolute workhorse of visual fidelity. While the previous stages determined *where* a shape is on the screen, the Pixel Shader determines exactly *what color* each pixel should be. It runs in massive parallel, executing your custom shader code millions of times per frame—once for every individual fragment generated by the Rasterizer.

### 1. Core Responsibilities (What Happens in Detail)

The Pixel Shader takes the raw, smoothly blended data handed down from the surface of the triangle and applies lighting, texturing, and materials to compute a final color value.

#### A. Texture Sampling

This is where 2D images are projected onto 3D surfaces. The Pixel Shader receives the interpolated UV coordinates from the Rasterizer and uses them to look up color values from a texture map (Albedo/Diffuse map) stored in VRAM. It can also sample other texture maps, such as roughness maps, metallic maps, or ambient occlusion maps.

#### B. Lighting and Shading Calculations

The Pixel Shader is where complex math models (like Phong, Blinn-Phong, or PBR - Physically Based Rendering) are executed. It takes the interpolated World Position and World Normal of the pixel, combines them with global data (like the position and color of a light source), and calculates:

* **Diffuse Lighting:** How bright the surface is based on its angle to the light.
* **Specular Lighting:** The bright, shiny highlights that change based on where the camera is looking.
* **Shadows:** Sampling shadow maps to see if a pixel is hidden from a light source.

#### C. Normal Mapping (Adding Fake Detail)

Even though the Tessellator and Domain Shader can physically create geometry, artists also use **Normal Maps** in the Pixel Shader. The shader reads a special texture containing high-resolution 3D normal vectors and overrides the triangle's actual flat geometric normal. This tricks the lighting math into creating the illusion of deep cracks, bumps, and rivets on a completely flat surface.

#### D. Discarding Fragments (Alpha Testing)

The Pixel Shader has a unique power: it can choose to commit suicide. If you are rendering a chain-link fence or a leaf texture, parts of the texture are completely transparent. The Pixel Shader can test the alpha value of a texture, and if it is below a certain threshold, execute a `discard` (or `clip()`) command. The fragment is instantly deleted, skipping the rest of the pipeline.

### 2. Execution Constraints (What it *Cannot* Do)

* **Isolated Execution:** Pixel Shaders run in complete isolation. Pixel $(100, 200)$ has no idea what color Pixel $(101, 200)$ is choosing to be.
* **No Coordinate Changing:** A Pixel Shader cannot change *where* it is on the screen. It can only calculate data for the specific screen coordinate it was assigned by the Rasterizer.
* **Not the Final Word:** Outputting a color does not guarantee it shows up on screen. The pixel still must pass the Output Merger stage (Depth and Stencil tests).

### 3. Inputs vs. Outputs

#### Inputs

* **Interpolated Varyings:** The custom variables calculated at the triangle corners and smoothly blended by the Rasterizer (UVs, Positions, Normals, Tangents).
* **Global Uniforms / Bindings:** Texture samplers, light positions, camera positions, and material properties.
* **`SV_Position` / `gl_FragCoord`:** The exact $X, Y$ pixel location on the screen and its $Z$ depth value.

#### Outputs

* **`SV_Target` / `gl_FragColor`:** The final color of the pixel, typically formatted as a 4-component vector: `RGBA` (Red, Green, Blue, Alpha) as floats from $0.0 \dots 1.0$.
* **`SV_Depth` (Optional):** The shader can manually override the depth value of the pixel, though doing this disables major GPU optimizations like Early-Z testing.

### Summary of Steps (The Sequential Checklist)

When a fragment enters the Pixel Shader, the code processes it through these precise steps:

* **Step 1: Receive Interpolated Attributes** — The shader gathers the unique, perspective-blended surface data (UVs, normals, positions) generated for this specific pixel location by the Rasterizer.
* **Step 2: Sample Base Textures** — The shader uses the UV coordinates to sample texture maps from VRAM to determine the base color (Albedo) and material properties of the surface.
* **Step 3: Sample Surface Normal Modifications** — If using normal mapping, the shader reads the normal texture and transforms it to calculate a highly detailed, modified surface orientation.
* **Step 4: Evaluate Transparency (Alpha Clipping)** — The shader checks the alpha channel of the material; if it fails transparency rules, the shader invokes a discard command to immediately terminate the fragment.
* **Step 5: Execute Lighting Math** — Using the surface normal, world position, camera view direction, and light properties, the shader executes mathematical algorithms to calculate diffuse, specular, and ambient lighting reflections.
* **Step 6: Apply Secondary Visual Effects** — The shader layers on extra calculations like fog, environmental reflections, or ambient occlusion to finalize the pixel's appearance.
* **Step 7: Output Final Color** — The shader writes the computed `RGBA` value to the output render target register, exiting the programmable pipeline and passing the data to the **Output Merger** for final blending and depth checks.

---
## Output Merger(OM)
The Output Merger is a **fixed-function hardware block**. You cannot write a custom shader for it; you configure its behavior via your graphics API pipeline state. Its core responsibility is to take the raw color output from the Pixel Shader, combine it with the data that *already exists* on your screen, and determine if the pixel legally deserves to be written to the final **Render Target** (Framebuffer).

### 1. Core Responsibilities (What Happens in Detail)

The Output Merger acts as the ultimate gatekeeper of the frame, handling visibility and transparency tests.

#### A. The Stencil Test (Masking)

The Stencil Test compares a value from a special **Stencil Buffer** against a reference value you set in your code. It acts like a physical stencil or mask. If the test fails, the pixel is immediately thrown away. This is used for advanced rendering techniques like drawing mirrors, portal clipping planes, or rendering complex user interfaces and outlines.

#### B. The Depth Test (Occlusion / Z-Testing)

This is how the GPU ensures that a solid wall correctly hides a character standing behind it. Every time a pixel wants to draw to the screen, the Output Merger checks its $Z$ depth value against the **Depth Buffer** (Z-Buffer), which tracks how close the current on-screen pixel is to the camera.

* If the new pixel is *closer* than the existing pixel, it passes the test. The OM overwrites the color on screen and updates the Depth Buffer with the new, closer value.
* If the new pixel is *further away*, it fails the test and is instantly discarded.

> [!NOTE]
> 💡 **Early-Z Optimization:** Because running a complex Pixel Shader on a hidden fragment wastes 
> massive amounts of GPU power, modern GPUs actually run a version of this depth test *before*
> the Pixel Shader (called **Early-Z**). However, the Output Merger still runs the final
> check here to catch any edge cases or manual shader modifications.

#### C. Color Blending (Transparency)

If a pixel passes both the stencil and depth tests, the Output Merger looks at its Alpha value to determine transparency. Since a pixel shader cannot see what is already behind it, the Output Merger handles the math to blend them together using a configured equation:

$$\mathbf{C}_{\text{final}} = (\mathbf{C}_{\text{source}} \times \mathbf{F}_{\text{source}}) + (\mathbf{C}_{\text{destination}} \times \mathbf{F}_{\text{destination}})$$

* $\mathbf{C}_{\text{source}}$: The new color coming out of your Pixel Shader.
* $\mathbf{C}_{\text{destination}}$: The color currently sitting in the Framebuffer.
* $\mathbf{F}$: The blend factors (e.g., matching the alpha channel for a standard overlay effect).

### 2. Execution Constraints (What it *Cannot* Do)

* **No Logic Modification:** You cannot run custom mathematical loops or algorithmic code here. You must choose from built-in hardware formulas (like `ADD`, `SUBTRACT`, `MIN`, `MAX`) and standard blend states.
* **No Spatial Changes:** It operates purely on a 1:1 pixel grid match based on the exact screen coordinate handed down through the pipeline.

### 3. Inputs vs. Outputs

#### Inputs

* **Pixel Shader Output:** The calculated `RGBA` color stream.
* **Current Framebuffer States:** The existing color, depth, and stencil buffers stored in memory for that specific pixel coordinate.
* **Pipeline Configuration:** Your predefined blend states, depth comparison functions (e.g., `LESS_EQUAL`), and write masks.

#### Outputs

* **The Final Framebuffer Update:** The updated, visible color pixel pushed directly onto your monitor's display stream, alongside the newly modified depth and stencil values.

### Summary of Steps (The Sequential Checklist)

When a color value leaves the Pixel Shader, the Output Merger processes it through these precise steps:

* **Step 1: Check Pipeline Write Masks** — The hardware checks if color, depth, or stencil writes are globally enabled or disabled for the current pipeline state.
* **Step 2: Evaluate the Stencil Test** — The OM reads the stencil buffer value at the pixel's coordinate and runs a comparison test; if it fails, the pixel is discarded.
* **Step 3: Evaluate the Depth Test (Z-Test)** — The hardware compares the incoming fragment's depth value against the value stored in the Z-buffer to see if the new geometry is closer to the camera than what is already drawn.
* **Step 4: Execute Buffer Write Updates** — If the tests pass, the OM instantly writes the updated depth and stencil tracking data back into their respective memory buffers.
* **Step 5: Apply Color Blending Operations** — If transparency or color blending is enabled, the hardware executes fixed-function math to mix the pixel shader's color with the existing background color.
* **Step 6: Perform Logical Bitwise Operations** — The hardware applies any final, optional bitwise modifications to the raw color data channels.
* **Step 7: Commit to the Render Target** — The final blended color is written directly into the Framebuffer texture slots, concluding the entire graphics pipeline execution for that frame.

---

