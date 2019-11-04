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

var ground_tex;
var ground_img;

var squaresPerSide = 16;
var texSize = 256;
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

var unit = Math.max(tex_size[0], tex_size[1]) / 50.0;
var program, program_cyl, program_cube, program_sphere;
var ground_plane_start = 0;

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
function configureTexture(texture, image) {
    texture = gl.createTexture();
    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, texture);
    gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, texSize, texSize, 0, gl.RGBA, gl.UNSIGNED_BYTE, image);
    gl.generateMipmap(gl.TEXTURE_2D);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER,
                      gl.NEAREST_MIPMAP_LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
}

/*
	Function responsible for initializing WEbGL components
	Also creates the models involved in rendering
*/
window.onload = function init() {
    canvas = document.getElementById( "gl-canvas" );

    gl = WebGLUtils.setupWebGL( canvas );
    if ( !gl ) { alert( "WebGL isn't available" ); }

	gl.viewport(0, 0, canvas.width, canvas.height);
	aspect = canvas.width/canvas.height;
	gl.clearColor(153.0/255.0, 204.0/255.0, 1.0, 1.0);
	gl.enable(gl.DEPTH_TEST);

    // create our cylinder
    cylinder1 = new cylinder();
    cylinder1.hight = 1.0;
    cylinder1.generate();
    cylinder1.modelViewLoc = modelViewLoc_cyl;
    cylinder1.start_idx = pointsArray.length;
    colorsArray = colorsArray.concat(cylinder1.colors);
    pointsArray = pointsArray.concat(cylinder1.vertices);

    // create our cube
    cube1 = new cube();
    cube1.generate();
    cube1.modelViewLoc = modelViewLoc_cube;
    cube1.start_idx = pointsArray.length;
    colorsArray = colorsArray.concat(cube1.colors);
    pointsArray = pointsArray.concat(cube1.vertices);

    // create our sphere
    sphere1 = new sphere();
    sphere1.generate();
    sphere1.modelViewLoc = modelViewLoc_sphere;
    sphere1.start_idx = pointsArray.length;
    colorsArray = colorsArray.concat(sphere1.colors);
    pointsArray = pointsArray.concat(sphere1.vertices);

	// create the ground plane
	ground_plane_start = pointsArray.length;
    pointsArray.push(vec4(-tex_size[0]/2, -tex_size[1]/2, 0.0, 1.0));
    pointsArray.push(vec4(-tex_size[0]/2, tex_size[1]/2, 0.0, 1.0));
    pointsArray.push(vec4(tex_size[0]/2, tex_size[1]/2, 0.0, 1.0));
    pointsArray.push(vec4(tex_size[0]/2, -tex_size[1]/2, 0.0, 1.0));

    // push empty colors so no out of range error for the next
    // colorsArray.push(vec4(1.0, 0.0, 0.0, 1.0));
    // colorsArray.push(vec4(1.0, 0.0, 0.0, 1.0));
    // colorsArray.push(vec4(1.0, 0.0, 0.0, 1.0));
    // colorsArray.push(vec4(1.0, 0.0, 0.0, 1.0));

    // texture creation
	create_ground_plane();
	configureTexture(ground_tex, ground_img); 
	gl.texParameteri( gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST );
    // end texture creation

    // push the texture coords
    colorsArray.push(vec4(0, 0, 0, 1));
    colorsArray.push(vec4(0, tex_size[1], 0, 1));
    colorsArray.push(vec4(tex_size[0], tex_size[1], 0, 1));
    colorsArray.push(vec4(tex_size[0], 0), 0, 1);
    // end creating stuff

    // start ground plane shader initi
	program = initShaders(gl, "vertex-shader", "fragment-shader");
	gl.useProgram(program);
    modelViewLoc = gl.getUniformLocation( program, "modelView" );
    projectionLoc = gl.getUniformLocation( program, "projection" );
    texMaxLoc = gl.getUniformLocation( program, "fTexMax" );

    // texture buffer
    var tBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, tBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(texCoordsArray), gl.STATIC_DRAW);

    var vTexCoord = gl.getAttribLocation( program, "vTexCoord");
    gl.vertexAttribPointer(vTexCoord, 4, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vTexCoord);
    // end texture buffer

    var vBuffer = gl.createBuffer();
    gl.bindBuffer( gl.ARRAY_BUFFER, vBuffer );
    gl.bufferData( gl.ARRAY_BUFFER, flatten(pointsArray), gl.STATIC_DRAW );

    var vPosition = gl.getAttribLocation( program, "vPosition" );
    gl.vertexAttribPointer( vPosition, 4, gl.FLOAT, false, 0, 0 );
    gl.enableVertexAttribArray( vPosition );
    // end ground plane

    // begin cylinder
    program_cyl = initShaders(gl, "cyl-vertex-shader", "cyl-fragment-shader");
	gl.useProgram(program_cyl);
    modelViewLoc_cyl = gl.getUniformLocation( program_cyl, "modelView" );
    projectionLoc_cyl = gl.getUniformLocation( program_cyl, "projection" );
    cylinder1.modelViewLoc = projectionLoc_cyl;
    cylinder1.projectionLoc = modelViewLoc_cyl;

 	var cBuffer = gl.createBuffer( );
    gl.bindBuffer( gl.ARRAY_BUFFER, cBuffer );
    gl.bufferData( gl.ARRAY_BUFFER, flatten(colorsArray), gl.STATIC_DRAW );

    var vColor = gl.getAttribLocation( program_cyl, "vColor" );
    gl.vertexAttribPointer( vColor, 4, gl.FLOAT, false, 0, 0 );
    gl.enableVertexAttribArray( vColor );

    var vBuffer = gl.createBuffer();
    gl.bindBuffer( gl.ARRAY_BUFFER, vBuffer );
    gl.bufferData( gl.ARRAY_BUFFER, flatten(pointsArray), gl.STATIC_DRAW );

    var vPosition = gl.getAttribLocation( program_cyl, "vPosition" );
    gl.vertexAttribPointer( vPosition, 4, gl.FLOAT, false, 0, 0 );
    gl.enableVertexAttribArray( vPosition );
    // end cylinder

    // begin cube
    program_cube = initShaders(gl, "cube-vertex-shader", "cube-fragment-shader");
	gl.useProgram(program_cube);
    modelViewLoc_cube = gl.getUniformLocation( program_cube, "modelView" );
    projectionLoc_cube = gl.getUniformLocation( program_cube, "projection" );
    cube1.modelViewLoc = projectionLoc_cube;
    cube1.projectionLoc = modelViewLoc_cube;

 	var cBuffer = gl.createBuffer( );
    gl.bindBuffer( gl.ARRAY_BUFFER, cBuffer );
    gl.bufferData( gl.ARRAY_BUFFER, flatten(colorsArray), gl.STATIC_DRAW );

    var vColor = gl.getAttribLocation( program_cube, "vColor" );
    gl.vertexAttribPointer( vColor, 4, gl.FLOAT, false, 0, 0 );
    gl.enableVertexAttribArray( vColor );

    var vBuffer = gl.createBuffer();
    gl.bindBuffer( gl.ARRAY_BUFFER, vBuffer );
    gl.bufferData( gl.ARRAY_BUFFER, flatten(pointsArray), gl.STATIC_DRAW );

    var vPosition = gl.getAttribLocation( program_cube, "vPosition" );
    gl.vertexAttribPointer( vPosition, 4, gl.FLOAT, false, 0, 0 );
    gl.enableVertexAttribArray( vPosition );
    // end cube

    // begin sphere
    program_sphere = initShaders(gl, "sphere-vertex-shader", "sphere-fragment-shader");
	gl.useProgram(program_sphere);
    modelViewLoc_sphere = gl.getUniformLocation( program_sphere, "modelView" );
    projectionLoc_sphere = gl.getUniformLocation( program_sphere, "projection" );
    sphere1.modelViewLoc = projectionLoc_sphere;
    sphere1.projectionLoc = modelViewLoc_sphere;

 	var cBuffer = gl.createBuffer( );
    gl.bindBuffer( gl.ARRAY_BUFFER, cBuffer );
    gl.bufferData( gl.ARRAY_BUFFER, flatten(colorsArray), gl.STATIC_DRAW );

    var vColor = gl.getAttribLocation( program_sphere, "vColor" );
    gl.vertexAttribPointer( vColor, 4, gl.FLOAT, false, 0, 0 );
    gl.enableVertexAttribArray( vColor );

    var vBuffer = gl.createBuffer();
    gl.bindBuffer( gl.ARRAY_BUFFER, vBuffer );
    gl.bufferData( gl.ARRAY_BUFFER, flatten(pointsArray), gl.STATIC_DRAW );

    var vPosition = gl.getAttribLocation( program_sphere, "vPosition" );
    gl.vertexAttribPointer( vPosition, 4, gl.FLOAT, false, 0, 0 );
    gl.enableVertexAttribArray( vPosition );
    // end sphere

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
function render() {
    gl.clear( gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT );

    eye = vec3(0.0, -1.5 * tex_size[0], 2.5 * tex_size[1]);
    mvMatrix = lookAt(eye, at, up);
    pMatrix = perspective(fovy, aspect, near, far);

    var rot_x = rotate(rho_inp, vec3(1.0, 0.0, 0.0));
    var rot_y = rotate(the_inp, vec3(0.0, 1.0, 0.0));
    var rot_z = rotate(phi_inp, vec3(0.0, 0.0, 1.0));
    var rot = mult(rot_x, mult(rot_y, rot_z));

    inp_mat = mult(rot, translate(x_inp, y_inp, z_inp));

    var old_mvMatrix = mult(mvMatrix, inp_mat);
    mvMatrix = old_mvMatrix;

	gl.useProgram(program_cyl);
 	mvMatrix = mult(mvMatrix, translate(0, 0, 0.252));
    gl.uniformMatrix4fv( modelViewLoc_cyl, false, flatten( mult(mvMatrix, scalem(0.5, 0.5, 0.25))) ); //resize cylinder
    gl.uniformMatrix4fv( projectionLoc_cyl, false, flatten( pMatrix  ) );
    gl.drawArrays(gl.TRIANGLES, cylinder1.start_idx, cylinder1.vertices.length);

	gl.useProgram(program_cube);
 	mvMatrix = mult(mvMatrix, translate(-0.5, 0, -0.126));
    gl.uniformMatrix4fv( modelViewLoc_cube, false, flatten( mult(mvMatrix, scalem(0.25, 0.25, 0.25))) ); //resize cube
    gl.uniformMatrix4fv( projectionLoc_cube, false, flatten( pMatrix  ) );
	cube1.transform_cube(mvMatrix);
	cube1.projection_mat = pMatrix;
    gl.drawArrays(gl.TRIANGLES, cube1.start_idx, cube1.vertices.length);

	gl.useProgram(program_sphere);
 	mvMatrix = mult(mvMatrix, translate(1, 0, 0));
    gl.uniformMatrix4fv( modelViewLoc_sphere, false, flatten( mult(mvMatrix, scalem(0.125, 0.125, 0.125))) ); //resize sphere
    gl.uniformMatrix4fv( projectionLoc_sphere, false, flatten( pMatrix  ) );
	sphere1.transform_sph(mvMatrix);
	sphere1.projection_mat = pMatrix;

    gl.drawArrays(gl.TRIANGLES, sphere1.start_idx, sphere1.vertices.length);

	gl.useProgram(program);
    mvMatrix = old_mvMatrix;
    gl.uniformMatrix4fv( modelViewLoc, false, flatten(mvMatrix) );
    gl.uniformMatrix4fv( projectionLoc, false, flatten(pMatrix) );
    gl.uniform2f( texMaxLoc, false, flatten(tex_size) );
    gl.drawArrays( gl.TRIANGLE_FAN, ground_plane_start, 4 );

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