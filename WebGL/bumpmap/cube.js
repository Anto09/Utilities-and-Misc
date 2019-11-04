function cube()
{
	this.num_vertices = 6.0; 

	this.start_idx = 0;

	this.trans_mat = mat4(
        vec4( 1.0, 0.0, 0.0, 0.0 ),
        vec4( 0.0, 1.0, 0.0, 0.0 ),
        vec4( 0.0, 0.0, 1.0, 0.0 ),
        vec4( 0.0, 0.0, 0.0, 1.0 )
    );
	this.rot_mat = mat4(
        vec4( 1.0, 0.0, 0.0, 0.0 ),
        vec4( 0.0, 1.0, 0.0, 0.0 ),
        vec4( 0.0, 0.0, 1.0, 0.0 ),
        vec4( 0.0, 0.0, 0.0, 1.0 )
    );
    this.scale_mat = mat4(
        vec4( 1.0, 0.0, 0.0, 0.0 ),
        vec4( 0.0, 1.0, 0.0, 0.0 ),
        vec4( 0.0, 0.0, 1.0, 0.0 ),
        vec4( 0.0, 0.0, 0.0, 1.0 )
    );
	this.modelView_mat = [];
	this.projection_mat = [];

	this.modelViewLoc;	// start with lookat -> always feed this default lookAt
	this.projectionLoc;
	this.vPosition = vec4(0.0, 0.0, 0.0, 1.0);

	this.quad 			= quad;
	this.generate 		= generate_cube;
	this.render 		= render_cube;
	this.trans_cube 	= trans_cube;
	this.rot_cube 		= rot_cube;
	this.scale_cube 	= scale_cube;
	this.transform_cube = transform_cube;
	this.get_end_idx 	= get_end_idx_cube;
	this.reset_cube 	= reset_cube;
	this.quad 			= quad;
	this.pointsArray 	= [];
	this.colorsArray 	= [];
	this.normalsArray 	= [];
	this.vertices 		= [];
	this.colors 		= [];
	this.normals		= [];	

	this.tex 			= [];
	this.texCoord 		= [
						    vec2(0, 0),
						    vec2(0, 1),
						    vec2(1, 1),
						    vec2(1, 0)
						  ];
}

function reset_cube() {
	this.trans_mat = mat4(
        vec4( 1.0, 0.0, 0.0, 0.0 ),
        vec4( 0.0, 1.0, 0.0, 0.0 ),
        vec4( 0.0, 0.0, 1.0, 0.0 ),
        vec4( 0.0, 0.0, 0.0, 1.0 )
    );
	this.rot_mat = mat4(
        vec4( 1.0, 0.0, 0.0, 0.0 ),
        vec4( 0.0, 1.0, 0.0, 0.0 ),
        vec4( 0.0, 0.0, 1.0, 0.0 ),
        vec4( 0.0, 0.0, 0.0, 1.0 )
    );
    this.scale_mat = mat4(
        vec4( 1.0, 0.0, 0.0, 0.0 ),
        vec4( 0.0, 1.0, 0.0, 0.0 ),
        vec4( 0.0, 0.0, 1.0, 0.0 ),
        vec4( 0.0, 0.0, 0.0, 1.0 )
    );
}

function generate_cube()
{
	
	this.pointsArray  = [vec4(-0.5, -0.5,  0.5, 1.0),
						 vec4(-0.5,  0.5,  0.5, 1.0),
						 vec4(0.5,  0.5,  0.5, 1.0),
						 vec4(0.5, -0.5,  0.5, 1.0),
						 vec4(-0.5, -0.5, -0.5, 1.0),
						 vec4(-0.5,  0.5, -0.5, 1.0),
						 vec4(0.5,  0.5, -0.5, 1.0),
						 vec4(0.5, -0.5, -0.5, 1.0)];

	this.colorsArray  = [vec4( 0.5, 0.5, 0.5, 1.0 ),
						 vec4( 0.5, 0.5, 0.5, 1.0 ),
						 vec4( 0.5, 0.5, 0.5, 1.0 ),
						 vec4( 0.5, 0.5, 0.5, 1.0 ),
						 vec4( 0.5, 0.5, 0.5, 1.0 ),
						 vec4( 0.5, 0.5, 0.5, 1.0 ),
						 vec4( 0.5, 0.5, 0.5, 1.0 ),
						 vec4( 0.5, 0.5, 0.5, 1.0 )];


    this.quad(1, 0, 3, 2 );
    this.quad(2, 3, 7, 6 );
    this.quad(3, 0, 4, 7 );
    this.quad(6, 5, 1, 2 );
    this.quad(4, 5, 6, 7 );
    this.quad(5, 4, 0, 1 );
}

function get_end_idx_cube()
{
	return this.start_idx + this.vertices.length;
}

function trans_cube(x, y, z)
{
	// this.trans_mat = mult(this.trans_mat, translate(x, y, z));
	this.trans_mat = translate(x, y, z);
}

function rot_cube(angle, axis) {
	// this.rot_mat = mult(this.rot_mat, rotate(angle, axis));
	this.rot_mat = rotate(angle, axis);
}

function scale_cube(x, y, z) {
	// this.scale_mat = mult(this.scale_mat, scalem(x, y, z));
	this.scale_mat = scalem(x, y, z);
}

function transform_cube(trans_mat) {
	this.modelView_mat = trans_mat;
}

function quad(a, b, c, d) {

	var t1 = subtract(this.pointsArray[b], this.pointsArray[a]);
	var t2 = subtract(this.pointsArray[c], this.pointsArray[b]);
	var normal = cross(t1, t2);
	var normal = vec3(normal);

	this.vertices.push(this.pointsArray[a]);
	this.colors.push(this.colorsArray[a]);
    this.tex.push(this.texCoord[0]);
    this.normals.push(normal);

	this.vertices.push(this.pointsArray[b]);
	this.colors.push(this.colorsArray[a]);
    this.tex.push(this.texCoord[1]);
    this.normals.push(normal);

	this.vertices.push(this.pointsArray[c]);
	this.colors.push(this.colorsArray[a]);
    this.tex.push(this.texCoord[2]);
    this.normals.push(normal);

	this.vertices.push(this.pointsArray[a]);
	this.colors.push(this.colorsArray[a]);
    this.tex.push(this.texCoord[0]);
    this.normals.push(normal);

	this.vertices.push(this.pointsArray[c]);
	this.colors.push(this.colorsArray[a]);
    this.tex.push(this.texCoord[2]);
    this.normals.push(normal);

	this.vertices.push(this.pointsArray[d]);
	this.colors.push(this.colorsArray[a]);
    this.tex.push(this.texCoord[3]);
    this.normals.push(normal);
}

function render_cube()
{	
	var mv_mat = mult(this.modelView_mat, this.trans_mat);
	mv_mat = mult(mv_mat, this.rot_mat);	
	mv_mat = mult(mv_mat, this.scale_mat);

    gl.uniformMatrix4fv( this.modelViewLoc, false, flatten( mv_mat ) );
    gl.uniformMatrix4fv( this.projectionLoc, false, flatten( this.projection_mat ) );

    gl.drawArrays(gl.TRIANGLES, this.start_idx, this.vertices.length);
}