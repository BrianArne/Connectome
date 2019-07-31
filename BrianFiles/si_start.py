import gl
gl.resetdefaults()
gl.meshload('BrainMesh_ICBM152.mz3')
gl.nodeload('./atlas.node')
gl.edgeload('./atlas.edge')
gl.nodethreshbysizenotcolor(False)
gl.edgethresh(0.0, 1.0)
gl.shaderxray(0.5, 0.1)
