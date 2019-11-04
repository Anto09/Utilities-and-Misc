var canvas;
var gl;


var thetaLoc;
var transLoc;

var near 	= 0.3;
var far 	= 100000.0;
var radius 	= 8.0;
var theta  	= 0.1;
var phi    	= -0.3;
var dr 		= 5.0 * Math.PI/180.0;

var  fovy = 35.0;  // Field-of-view in Y direction angle (in degrees)
var  aspect;       // Viewport aspect ratio

var mvMatrix, pMatrix;
var modelViewLoc, projectionLoc, texMaxLoc;
var modelViewLoc_cyl, projectionLoc_cyl;
var modelViewLoc_sphere, projectionLoc_sphere;
var modelViewLoc_cube, projectionLoc_cube;
var tex_size = vec2(1, 1);
var grid_height = 2.0;
var grid_width = 2.0;

var objects = [];

var eye;
var view;
const at = vec3(0.0, 0.0, 0.0);
const up = vec3(0.0, 1.0, 0.0);

var ground_tex = null;
var ground_img;

var cube_tex = null;
var cuve_img;

var cyl_tex = null;
var cyl_img;

var sph_tex;
var sph_imgPX;
var sph_imgPY;
var sph_imgPZ;
var sph_imgNX;
var sph_imgNY;
var sph_imgNZ;


var squaresPerSide = 16;
var texSize = 512;
var tDepth = 4;
var pointsArray = [];
var texCoordsArray = [];
var colorsArray = [];

var sphere1;
var cylinder1;
var cube1;

var x_inp = 0;
var y_inp = 0;
var z_inp = 0;

var phi_inp = 0;
var rho_inp = 0;
var the_inp = 0;

var inp_mat = mat4(
        vec4( 1.0, 0.0, 0.0, 0.0 ),
        vec4( 0.0, 1.0, 0.0, 0.0 ),
        vec4( 0.0, 0.0, 1.0, 0.0 ),
        vec4( 0.0, 0.0, 0.0, 1.0 )
    );

var unit = Math.max(tex_size[0], tex_size[1]) / 25.0;
var program, program_cyl, program_cube, program_sphere;
var ground_plane_start = 0;

// phone shading stuff
var cube_normals;

/*
	Function responsible for creating the checkerboard texture
	Taken from Dr. Lindeman's site
	Alternates between black and white per given square
*/
function create_ground_plane() {
	var texelsPerSquareSide = texSize / squaresPerSide;

	ground_img = new Uint8Array( tDepth * texSize * texSize );
	for( var i = 0; i < texSize; i++ )  {
	  for( var j = 0; j < texSize; j++ )  {
	    // Compute the Black/White color, switching every texelsPerSquareSide texels.
	    var bw = ( ( ( i & texelsPerSquareSide ) == 0 ) ^ ( ( j & texelsPerSquareSide )  == 0 ) );
	    for( var k = 0; k < tDepth-1; k++ )  {
	      ground_img[ ( tDepth * texSize * i ) + ( tDepth * j ) + k ] = ( 255.0 * bw );
	    }
	    // Set the alpha to 1.
	    ground_img[ ( tDepth * texSize * i ) + ( tDepth * j ) + k ] = ( 255.0 * 1.0 );
	  }
	}
}

/*
	Function responsible for configuring the texture for the ground plane
	Generates a 2D map for the ground plane texture, uses GL.RGBA
*/

 
function isPowerOfTwo(x) {
    return (x & (x - 1)) == 0;
}

function nextHighestPowerOfTwo(x) {
    --x;
    for (var i = 1; i < 32; i <<= 1) {
        x = x | x >> i;
    }
    return x + 1;
}

/*
	Function responsible for initializing WEbGL components
	Also creates the models involved in rendering
*/
var tBuffer;
var tBuffer_cube;
var tBuffer_cyl;
var tBuffer_sph;

var vBuffer;
var vBuffer_cube;
var vBuffer_cyl;
var vBuffer_sph;

var cBuffer;
var cBuffer_cube;
var cBuffer_cyl;
var cBuffer_sph;

var nBuffer;
var nBuffer_cube;
var nBuffer_cyl;
var nBuffer_sph;

var tnBuffer;
var tnBuffer_cube;
var tnBuffer_cyl;
var tnBuffer_sph;

var cube_uLightDir;
var cube_uLightAmb;
var cube_uLightDiff;
var cube_uLightSpec;
var cube_uMatAmb;
var cube_uMatDiff;
var cube_uMatSpec;
var cube_uShine;

var bumpmap_tex; 
var bumpmap_img;   



function load_bumpmap() {
    gl.useProgram(program_cyl);
    bumpmap_img = document.getElementById("cubeMap");
    bumpmap_tex = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D,bumpmap_tex);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.LUMINANCE, gl.LUMINANCE, gl.UNSIGNED_BYTE, bumpmap_img);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST);
    gl.uniform2f(u_bumpmapSize, bumpmap_img.width, bumpmap_img.height);
}

function load_bump_tex() {
    gl.useProgram(program_cyl);
    cyl_img = document.getElementById("cubeImage");
    cyl_tex = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, cyl_tex);

    if (!isPowerOfTwo(cyl_img.width) || !isPowerOfTwo(cyl_img.height)) {
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
        gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, cyl_img);
   }
    else {
        gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
        gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, texSize, texSize, 0, gl.RGBA, gl.UNSIGNED_BYTE, image);
        gl.generateMipmap(gl.TEXTURE_2D);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_NEAREST);
    }
    gl.texParameteri( gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST );
}

function make_cylinder() {
    // create our cylinder
    cylinder1 = new cylinder();
    cylinder1.hight = 1.0;
    cylinder1.generate();

    program_cyl = initShaders(gl, "cyl-vertex-shader", "cyl-fragment-shader");
    gl.useProgram(program_cyl);

    modelViewLoc_cyl    = gl.getUniformLocation( program_cyl, "modelView" );
    projectionLoc_cyl   = gl.getUniformLocation( program_cyl, "projection" );

    load_bump_tex();
    load_bumpmap();

    vBuffer_cyl = gl.createBuffer();
    gl.bindBuffer( gl.ARRAY_BUFFER, vBuffer_cyl );
    gl.bufferData( gl.ARRAY_BUFFER, flatten(cylinder1.vertices), gl.STATIC_DRAW );
    
    tBuffer_cyl = gl.createBuffer();
    gl.bindBuffer( gl.ARRAY_BUFFER, tBuffer_cyl );
    gl.bufferData( gl.ARRAY_BUFFER, flatten(cylinder1.tex), gl.STATIC_DRAW )

    nBuffer_cyl = gl.createBuffer();
    gl.bindBuffer( gl.ARRAY_BUFFER, nBuffer_cyl );
    gl.bufferData( gl.ARRAY_BUFFER, flatten(cylinder1.normals), gl.STATIC_DRAW )

    tnBuffer_cyl = gl.createBuffer();
    gl.bindBuffer( gl.ARRAY_BUFFER, tnBuffer_cyl );
    gl.bufferData( gl.ARRAY_BUFFER, flatten(cylinder1.tangents), gl.STATIC_DRAW )
}

function make_cube() {
    // create our cube
    cube1 = new cube();
    cube1.generate();

    program_cube = initShaders(gl, "cube-vertex-shader", "cube-fragment-shader");
    gl.useProgram(program_cube);
    modelViewLoc_cube   = gl.getUniformLocation( program_cube, "modelView" );
    projectionLoc_cube  = gl.getUniformLocation( program_cube, "projection" );

    cube_img = document.getElementById("cubeImage");
    cube_tex = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, cube_tex);

    if (!isPowerOfTwo(cube_img.width) || !isPowerOfTwo(cube_img.height)) {
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
        gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, cube_img);
   }
    else {
        gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
        gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, texSize, texSize, 0, gl.RGBA, gl.UNSIGNED_BYTE, cube_img);
        gl.generateMipmap(gl.TEXTURE_2D);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_NEAREST);
    }
    gl.texParameteri( gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST );

    cube_uLightDir  = gl.getAttribLocation(program_cube, "uLightDir");
    cube_uLightAmb  = gl.getAttribLocation(program_cube, "uLightAmb");
    cube_uLightDiff = gl.getAttribLocation(program_cube, "uLightDiff");
    cube_uLigtSpec  = gl.getAttribLocation(program_cube, "uLigtSpec");
    cube_uMatAmb    = gl.getAttribLocation(program_cube, "uMatAmb");
    cube_uMatDiff   = gl.getAttribLocation(program_cube, "uMatDiff");
    cube_uMatSpec   = gl.getAttribLocation(program_cube, "uMatSpec");
    cube_uShine     = gl.getAttribLocation(program_cube, "uShine");

    cube_uLightDir  = vec3(0.0, -1.0, -1.0);
    cube_uLightAmb  = vec4(0.03, 0.03, 0.03, 1.0);
    cube_uLightDiff = vec4(1.0, 1.0, 1.0, 1.0);
    cube_uLigtSpec  = vec4(1.0, 1.0, 1.0, 1.0);
    cube_uMatAmb    = vec4(1.0, 1.0, 1.0, 1.0);
    cube_uMatDiff   = vec4(0.5, 0.8, 0.1, 1.0);
    cube.uMatSpec   = vec4(1.0, 1.0, 1.0, 1.0);
    cube_uShine     = 230;

    /*
    cBuffer_cube = gl.createBuffer( );
    gl.bindBuffer( gl.ARRAY_BUFFER, cBuffer_cube );
    gl.bufferData( gl.ARRAY_BUFFER, flatten(cube1.colors), gl.STATIC_DRAW );
    */
    vBuffer_cube = gl.createBuffer();
    gl.bindBuffer( gl.ARRAY_BUFFER, vBuffer_cube );
    gl.bufferData( gl.ARRAY_BUFFER, flatten(cube1.vertices), gl.STATIC_DRAW );

    tBuffer_cube = gl.createBuffer();
    gl.bindBuffer( gl.ARRAY_BUFFER, tBuffer_cube );
    gl.bufferData( gl.ARRAY_BUFFER, flatten(cube1.tex), gl.STATIC_DRAW );

    nBuffer_cube = gl.createBuffer();
    gl.bindBuffer( gl.ARRAY_BUFFER, nBuffer_cube);
    gl.bufferData( gl.ARRAY_BUFFER, flatten(cube1.normals), gl.STATIC_DRAW);

}

function make_sphere() {
    // create our sphere
    sphere1 = new sphere();
    sphere1.generate();

    program_sphere = initShaders(gl, "sphere-vertex-shader", "sphere-fragment-shader");
    gl.useProgram(program_sphere);

    sph_imgPX = document.getElementById("posx");
    sph_imgPY = document.getElementById("posy");
    sph_imgPZ = document.getElementById("posz");
    sph_imgNX = document.getElementById("negx");
    sph_imgNY = document.getElementById("negy");
    sph_imgNZ = document.getElementById("negz");

    sph_tex = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_CUBE_MAP, sph_tex);
    gl.texImage2D(gl.TEXTURE_CUBE_MAP_POSITIVE_X ,0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, sph_imgPX);
    gl.texImage2D(gl.TEXTURE_CUBE_MAP_NEGATIVE_X ,0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, sph_imgNX);
    gl.texImage2D(gl.TEXTURE_CUBE_MAP_POSITIVE_Y ,0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, sph_imgPY);
    gl.texImage2D(gl.TEXTURE_CUBE_MAP_NEGATIVE_Y ,0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, sph_imgNY);
    gl.texImage2D(gl.TEXTURE_CUBE_MAP_POSITIVE_Z ,0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, sph_imgPZ );
    gl.texImage2D(gl.TEXTURE_CUBE_MAP_NEGATIVE_Z ,0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, sph_imgNZ);
    gl.texParameteri(gl.TEXTURE_CUBE_MAP, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
    gl.texParameteri(gl.TEXTURE_CUBE_MAP, gl.TEXTURE_MIN_FILTER, gl.NEAREST);

    modelViewLoc_sphere  = gl.getUniformLocation( program_sphere, "modelView" );
    projectionLoc_sphere = gl.getUniformLocation( program_sphere, "projection" );

    vBuffer_sph = gl.createBuffer();
    gl.bindBuffer( gl.ARRAY_BUFFER, vBuffer_sph );
    gl.bufferData( gl.ARRAY_BUFFER, flatten(sphere1.vertices), gl.STATIC_DRAW );

    nBuffer_sph = gl.createBuffer();
    gl.bindBuffer( gl.ARRAY_BUFFER, nBuffer_sph );
    gl.bufferData( gl.ARRAY_BUFFER, flatten(sphere1.normals), gl.STATIC_DRAW );
}

function make_ground_plane() {
    // create the ground plane
    pointsArray.push(vec4(-tex_size[0]/2, -tex_size[1]/2, 0.0, 1.0));
    pointsArray.push(vec4(-tex_size[0]/2, tex_size[1]/2, 0.0, 1.0));
    pointsArray.push(vec4(tex_size[0]/2, tex_size[1]/2, 0.0, 1.0));
    pointsArray.push(vec4(tex_size[0]/2, -tex_size[1]/2, 0.0, 1.0));

    texCoordsArray.push(vec2(0,0));
    texCoordsArray.push(vec2(0,1));
    texCoordsArray.push(vec2(1,1));
    texCoordsArray.push(vec2(1,0));
  
    create_ground_plane();
    
    program = initShaders(gl, "vertex-shader", "fragment-shader");
    gl.useProgram(program);

    ground_tex = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, ground_tex);
    if (!isPowerOfTwo(ground_img.width) || !isPowerOfTwo(ground_img.height)) {
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
        gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, ground_img);
   }
    else {
        gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
        gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, texSize, texSize, 0, gl.RGBA, gl.UNSIGNED_BYTE, ground_img);
        gl.generateMipmap(gl.TEXTURE_2D);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_NEAREST);
    }
    gl.texParameteri( gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST );

    modelViewLoc  = gl.getUniformLocation( program, "modelView" );
    projectionLoc = gl.getUniformLocation( program, "projection" );

    tBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, tBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(texCoordsArray), gl.STATIC_DRAW);
    
    vBuffer = gl.createBuffer();
    gl.bindBuffer( gl.ARRAY_BUFFER, vBuffer );
    gl.bufferData( gl.ARRAY_BUFFER, flatten(pointsArray), gl.STATIC_DRAW );
}

window.onload = function init() {
    canvas = document.getElementById( "gl-canvas" );

    gl = WebGLUtils.setupWebGL( canvas );
    if ( !gl ) { alert( "WebGL isn't available" ); }

	gl.viewport(0, 0, canvas.width, canvas.height);
	aspect = canvas.width/canvas.height;
	gl.clearColor(153.0/255.0, 204.0/255.0, 1.0, 1.0);
	gl.enable(gl.DEPTH_TEST);

    make_cube();
    make_cylinder();
    make_sphere();
    make_ground_plane();

    document.onkeydown = handle_key_down;
    document.onkeyup = handle_key_up;

    render();

}

/*
	Function used to render all components
	Takes into account transformation due to input

	Order of rendering:
		-Cylinder
		-Sphere
		-Cube
		-Plane
*/
function render_ground_plane() {
    gl.useProgram(program);

    gl.activeTexture(gl.TEXTURE4);
    gl.bindTexture(gl.TEXTURE_2D, ground_tex);
    gl.uniform1i(gl.getUniformLocation(program, "texture"), 4);

    var vTexCoord = gl.getAttribLocation( program, "vTexCoord");
    var vPosition = gl.getAttribLocation( program, "vPosition" );

    gl.bindBuffer(gl.ARRAY_BUFFER, tBuffer);
    gl.vertexAttribPointer(vTexCoord, 2, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray( vTexCoord );

    gl.bindBuffer( gl.ARRAY_BUFFER, vBuffer );
    gl.vertexAttribPointer( vPosition, 4, gl.FLOAT, false, 0, 0 );
    gl.enableVertexAttribArray( vPosition );

    gl.uniformMatrix4fv( modelViewLoc, false, flatten(mvMatrix) );
    gl.uniformMatrix4fv( projectionLoc, false, flatten(pMatrix) );
    gl.drawArrays( gl.TRIANGLE_FAN, 0, 4 );

    gl.disableVertexAttribArray( vTexCoord );
    gl.disableVertexAttribArray( vPosition );
}

function render_cylinder() {
    gl.useProgram(program_cyl);
    gl.activeTexture(gl.TEXTURE1);
    gl.bindTexture(gl.TEXTURE_2D, cyl_tex);
    gl.uniform1i(gl.getUniformLocation(program_cyl, "texture"), 1);
    gl.activeTexture(gl.TEXTURE2);
    gl.bindTexture(gl.TEXTURE_2D, bumpmap_tex);
    gl.uniform1i(gl.getUniformLocation(program_cyl, "bumpmap"), 2);

    var vTexCoord = gl.getAttribLocation( program_cyl, "vTexCoord");
    var vPosition = gl.getAttribLocation( program_cyl, "vPosition" );
    var vNormal   = gl.getAttribLocation(program_cyl, "vNormal");
    var vTangent  = gl.getAttribLocation(program_cyl, "vTangent");

    gl.bindBuffer(gl.ARRAY_BUFFER, tBuffer_cyl);
    gl.vertexAttribPointer(vTexCoord, 2, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray( vTexCoord );

    gl.bindBuffer( gl.ARRAY_BUFFER, vBuffer_cyl ); 
    gl.vertexAttribPointer( vPosition, 4, gl.FLOAT, false, 0, 0 );  
    gl.enableVertexAttribArray( vPosition );

    gl.bindBuffer( gl.ARRAY_BUFFER, nBuffer_cyl );
    gl.vertexAttribPointer( vNormal, 4, gl.FLOAT, false, 0, 0 );
    gl.enableVertexAttribArray( vNormal );

    gl.bindBuffer( gl.ARRAY_BUFFER, tnBuffer_cyl );
    gl.vertexAttribPointer( vTangent, 4, gl.FLOAT, false, 0, 0 );
    gl.enableVertexAttribArray( vTangent );

    mvMatrix     = mult(mvMatrix, translate(0, 0, 0.252));
    normalMatrix = mat3(mvMatrix);

    gl.uniformMatrix4fv( modelViewLoc_cyl, false, flatten( mult(mvMatrix, scalem(0.5, 0.5, 0.25))) ); //resize cylinder
    gl.uniformMatrix4fv( projectionLoc_cyl, false, flatten( pMatrix  ) );
    gl.uniformMatrix3fv(u_normalMatrix, false, normalMatrix);
    gl.drawArrays(gl.TRIANGLES, 0, cylinder1.vertices.length);

    gl.disableVertexAttribArray( vTexCoord );
    gl.disableVertexAttribArray( vPosition );
    gl.disableVertexAttribArray( vNormal );
    gl.disableVertexAttribArray( vTangent );
}

function render_cube() {
    gl.useProgram(program_cube);

    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, cube_tex);
    gl.uniform1i(gl.getUniformLocation(program_cube, "texture"), 0);

    var vTexCoord = gl.getAttribLocation( program, "vTexCoord");
    var vPosition = gl.getAttribLocation( program_cube, "vPosition" );
    var vVertexNormal = gl.getAttribLocation( program_cube, "vVertexNormal" );

    gl.bindBuffer( gl.ARRAY_BUFFER, tBuffer_cube );
    gl.vertexAttribPointer( vTexCoord, 2, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray( vTexCoord );

    gl.bindBuffer( gl.ARRAY_BUFFER, vBuffer_cube );
    gl.vertexAttribPointer( vPosition, 4, gl.FLOAT, false, 0, 0 );
    gl.enableVertexAttribArray( vPosition );

    // gl.bindBuffer( gl.ARRAY_BUFFER, nBuffer_cube );
    // gl.vertexAttribPointer( vVertexNormal, 4, gl.FLOAT, false, 0, 0 );
    // gl.enableVertexAttribArray( vVertexNormal );

    mvMatrix = mult(mvMatrix, translate(-0.5, 0, -0.126));
    gl.uniformMatrix4fv( modelViewLoc_cube, false, flatten( mult(mvMatrix, scalem(0.25, 0.25, 0.25))) ); //resize cube
    gl.uniformMatrix4fv( projectionLoc_cube, false, flatten( pMatrix  ) );
    gl.drawArrays(gl.TRIANGLES, 0, cube1.vertices.length);

    gl.disableVertexAttribArray( vTexCoord );
    gl.disableVertexAttribArray( vPosition );
}

function render_sphere() {
    gl.useProgram(program_sphere);

    gl.activeTexture(gl.TEXTURE3);
    gl.bindTexture(gl.TEXTURE_CUBE_MAP, sph_tex);
    gl.uniform1i(gl.getUniformLocation(program_sphere, "texture"), 3);
    var vPosition = gl.getAttribLocation( program_sphere, "vPosition" );
    var vNormal = gl.getAttribLocation( program_sphere, "vNormal" );

    gl.bindBuffer( gl.ARRAY_BUFFER, vBuffer_sph );
    gl.vertexAttribPointer( vPosition, 4, gl.FLOAT, false, 0, 0 );
    gl.enableVertexAttribArray( vPosition );

    gl.bindBuffer( gl.ARRAY_BUFFER, nBuffer_sph );
    gl.vertexAttribPointer( vNormal, 4, gl.FLOAT, false, 0, 0 );
    gl.enableVertexAttribArray( vNormal );

    mvMatrix = mult(mvMatrix, translate(1, 0, 0));
    var sph_mvMatrix = mvMatrix;
    var rot_x = rotate(-90, vec3(1.0, 0.0, 0.0));
    sph_mvMatrix = mult(sph_mvMatrix, rot_x);

    gl.uniformMatrix4fv( modelViewLoc_sphere, false, flatten( mult(sph_mvMatrix, scalem(0.125, 0.125, 0.125))) ); //resize sphere
    gl.uniformMatrix4fv( projectionLoc_sphere, false, flatten( pMatrix ) );
   
    gl.drawArrays(gl.TRIANGLES, 0, sphere1.vertices.length);
    gl.disableVertexAttribArray( vPosition );
    gl.disableVertexAttribArray( vNormal );
}

function render() {
    gl.clear( gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT );

    eye = vec3(0.0, -1.5 * tex_size[0], 2.5 * tex_size[1]);
    mvMatrix = lookAt(eye, at, up);
    pMatrix = perspective(fovy, aspect, near, far);

    var rot_x = rotate(rho_inp, vec3(1.0, 0.0, 0.0));
    var rot_y = rotate(the_inp, vec3(0.0, 1.0, 0.0));
    var rot_z = rotate(phi_inp, vec3(0.0, 0.0, 1.0));
    var rot = mult(rot_x, mult(rot_y, rot_z));

    inp_mat  = translate(x_inp, y_inp, z_inp);
    mvMatrix = mult(inp_mat, mult(mvMatrix, rot));

    render_ground_plane();
    render_cylinder();
    render_cube();
    render_sphere();
}

var currentlyPressedKeys = {};

/*
	Function to handle keydown press events
*/
function handle_key_down(event) {
    if (event.shiftKey)
    {
        var key = event.which;
        handle_key_code(true, false, key);
    }

    else if (event.ctrlKey)
    {
        var key = event.which;
        handle_key_code(false, true, key);
    }
    else
    {
        var key = event.which;
        handle_key_code(false, false, key);
    }
}

/*
	Function to handle keyup event (just in case needed)
*/
function handle_key_up(event) {
    if (event.shiftKey)
    {
    }
    else if (event.ctrlKey)
    {
    }
    else
    {
    }
}

/*
	Function which maps the given input to a specific transformation
	Updates the transformation parameters and calls render() again
*/
function handle_key_code(shift, ctrl, keycode) {
	switch(keycode) {
		case 37://left
			if(ctrl) {
				phi_inp -= 2;
   				render();
			}
			else {
				x_inp += unit;
   				render();
			}
			break;
		case 38://up
			if (shift) {
				z_inp -= unit;
   				render();
			}
			else if(ctrl) {
				the_inp += 2;
   				render();
			}
			else {
				y_inp -= unit;
   				render();
			}
			break;
		case 39://right
			if(ctrl) {
				phi_inp += 2;
   				render();
			}
			else {
				x_inp -= unit;
   				render();
			}
			break;
		case 40: //down
			if (shift) {
				z_inp += unit;
   				render();
			}
			else if(ctrl) {
				the_inp -= 2;
   				render();
			}
			else {
				y_inp += unit;
   				render();
			}
			break;
		case 82:
			rho_inp = 0;
			the_inp = 0;
			phi_inp = 0;

			x_inp = 0;
			y_inp = 0;
			x_inp = 0;
   			render();
			break;
		case 188:
			rho_inp += 2;
   			render();
			break;
		case 190:
			rho_inp -= 2;
   			render();
			break;
	}

}

/*
	keys:
		right arrow: = +1 unit X (39)
		left arrow: = -1 unit X (37)
		up arrow: = +1 unit Y (38)
		down arrow: = -1 unit Y (40)
		shift+up arrow = +1 unit Z (16 + 38)
		shift+down arrow = -1 unit Z (16 + 40)
		ctrl+down arrow = pitch +2 degs (17 + 40)
		ctrl+up arrow = pitch -2 degs (17 + 38)
		ctrl+right arrow = yaw +2 degs (17 + 39)
		ctrl+left arrow = yaw -2 degs (17 + 37)
		< = roll +2 degs (188)
		> = roll -2 degs (190)
		r = reset (82)
*/