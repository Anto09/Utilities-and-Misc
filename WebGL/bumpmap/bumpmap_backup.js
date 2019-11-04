var canvas;
var gl;

var points = [];
var colors = [];

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
var modelViewLoc, projectionLoc;
var grid_height = 2.0;
var grid_width = 2.0;

var objects = [];

var eye;
var view;
const at = vec3(0.0, 0.0, 0.0);
const up = vec3(0.0, 1.0, 0.0);

var ground_plane;
var ground_tex;
var ground_img;

var texCoord = [
    vec2(0, 0),
    vec2(1, 0),
    vec2(1, 1),
    vec2(0, 1)
];
var squaresPerSide = 16;
var texSize = 256;
var tDepth = 4;
var pointsArray = [];
var texCoordsArray = [];

function create_ground_plane() {
	var texelsPerSquareSide = texSize / squaresPerSide;

	ground_img = new Uint8Array( tDepth * texSize * texSize );
	for( var i = 0; i < texSize; i++ )  {
	  for( var j = 0; j < texSize; j++ )  {
	    // Compute the Black/White color, switching every texelsPerSquareSide texels.
	    var bw = ( ( ( i & texelsPerSquareSide ) == 0 ) ^ ( ( j & texelsPerSquareSide )  == 0 ) );
	    for( var k = 0; k < tDepth-1; k++ )  {
	      ground_img[ ( tDepth * texSize * i ) + ( tDepth * j ) + k ] = ( 255 * bw );
	    }
	    // Set the alpha to 1.
	    ground_img[ ( tDepth * texSize * i ) + ( tDepth * j ) + k ] = ( 255 * 1.0 );
	  }
	}
}


function configureTexture(texture, image) {
    texture = gl.createTexture();
    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, texture);
    gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, texSize, texSize, 0, gl.RGB, gl.UNSIGNED_BYTE, image);
    gl.generateMipmap(gl.TEXTURE_2D);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER,
                      gl.NEAREST_MIPMAP_LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
}

function mesh() {
     pointsArray.push(vertices[0]);
     texCoordsArray.push(texCoord[0]);

     pointsArray.push(vertices[1]);
     texCoordsArray.push(texCoord[1]);

     pointsArray.push(vertices[3]);
     texCoordsArray.push(texCoord[3]);

     pointsArray.push(vertices[2]); ;
     texCoordsArray.push(texCoord[2]);
}

window.onload = function init() {
    canvas = document.getElementById( "gl-canvas" );

    gl = WebGLUtils.setupWebGL( canvas );
    if ( !gl ) { alert( "WebGL isn't available" ); }

	// create cubes here?

	gl.viewport(0, 0, canvas.width, canvas.height);
	aspect = canvas.width/canvas.height;
	gl.clearColor(153.0/255.0, 204.0/255.0, 1.0, 1.0);
	gl.enable(gl.DEPTH_TEST);

	var program = initShaders(gl, "vertex-shader", "fragment-shader");
	gl.useProgram(program);
    modelViewLoc = gl.getUniformLocation( program, "modelView" );
    projectionLoc = gl.getUniformLocation( program, "projection" );

    // ground plane
    // ground_plane = new cube();
    // ground_plane.generate();
    // ground_plane.modelViewLoc = modelViewLoc;
    // ground_plane.scale_cube(10.0, 0.1, 10.0);
    // objects.push(ground_plane);

    // concatenate points
 //    for (var o = 0; o < objects.length; ++o) {
	//     colors = colors.concat(objects[o].colors);
	//     points = points.concat(objects[o].vertices);
	// }

    pointsArray.push(vec2(-10, -10));
    pointsArray.push(vec2(-10, 10));
    pointsArray.push(vec2(10, 10));
    pointsArray.push(vec2(10, -10));

    texCoordsArray.push(vec2(0, 0));
    texCoordsArray.push(vec2(0, 1));
    texCoordsArray.push(vec2(1, 1));
    texCoordsArray.push(vec2(1, 0));

    // texture buffer
    var tBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, tBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(texCoordsArray), gl.STATIC_DRAW);

    var vTexCoord = gl.getAttribLocation( program, "vTexCoord");
    gl.vertexAttribPointer(vTexCoord, 2, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vTexCoord);
    // end texture buffer

    var vBuffer = gl.createBuffer();
    gl.bindBuffer( gl.ARRAY_BUFFER, vBuffer );
    gl.bufferData( gl.ARRAY_BUFFER, flatten(pointsArray), gl.STATIC_DRAW );

    var vPosition = gl.getAttribLocation( program, "vPosition" );
    gl.vertexAttribPointer( vPosition, 2, gl.FLOAT, false, 0, 0 );
    gl.enableVertexAttribArray( vPosition );

    // texture creation
	create_ground_plane();
	configureTexture(ground_tex, ground_img); gl.texParameteri( gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST );
    // end texture creation

    eye = vec3(0.0, 15.0, 15.0);
    mvMatrix = lookAt(eye, at, up);
    pMatrix = perspective(fovy, aspect, near, far);

    gl.uniformMatrix4fv( modelViewLoc, false, flatten(mvMatrix) );
    gl.uniformMatrix4fv( projectionLoc, false, flatten(pMatrix) );

	// ground_plane.modelView_mat = mvMatrix
    render();
    // ground_plane.render();
}

function render() {

    gl.clear( gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT );
    gl.drawArrays( gl.TRIANGLE_FAN, 0, 4 );

}