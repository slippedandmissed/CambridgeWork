package uk.ac.cam.cl.gfxintro.jbs52.tick2;

import static org.lwjgl.opengl.GL11.GL_TRIANGLES;
import static org.lwjgl.opengl.GL11.GL_UNSIGNED_INT;
import static org.lwjgl.opengl.GL11.glDrawElements;
import static org.lwjgl.opengl.GL20.GL_FRAGMENT_SHADER;
import static org.lwjgl.opengl.GL20.GL_VERTEX_SHADER;
import static org.lwjgl.opengl.GL30.glBindVertexArray;

import java.util.ArrayList;
import java.util.List;

import org.joml.Matrix3f;
import org.joml.Matrix4f;
import org.joml.Vector3f;;

public class CubeRobot {
	
    // Filenames for vertex and fragment shader source code
    private final static String VSHADER_FN = "resources/cube_vertex_shader.glsl";
    private final static String FSHADER_FN = "resources/cube_fragment_shader.glsl";
    
    // Reference to skybox of the scene
    public SkyBox skybox;
    
    // Components of this CubeRobot
    
    private static class BodyPart {
    	private Mesh mesh;
    	private ShaderProgram shader;
    	private Texture texture;
    	private Matrix4f transform;
    	
    	private List<BodyPart> children;
    	
    	public BodyPart(Mesh mesh, ShaderProgram shader, Texture texture, Matrix4f transform) {
    		this.mesh = mesh;
    		this.shader = shader;
    		this.texture = texture;
    		this.transform = transform;
    		
    		this.children = new ArrayList<BodyPart>();
    	}
    	
    	public void addChild(BodyPart child) {
    		this.children.add(child);
    	}
    	
    	public Matrix4f getTransform() {
    		return transform;
    	}
    	
    	public void render(CubeRobot robot, Camera camera) {
    		render(robot, new Matrix4f(), camera);
    	}
    	
    	public void render(CubeRobot robot, Matrix4f parent, Camera camera) {
    		Matrix4f real_transform = new Matrix4f();
    		parent.mul(transform, real_transform);
    		robot.renderMesh(camera, mesh, real_transform, shader, texture);
    		for (BodyPart child : children) {
    			child.render(robot, real_transform, camera);
    		}
    	}
    }
    
    private BodyPart body;
    private BodyPart rightArm;
    private BodyPart leftArm;
    private BodyPart rightLeg;
    private BodyPart leftLeg;
    private BodyPart head;
    
    private float bodyHeight = 1.0f;
    private float bodyWidth = 1.0f;
    private float armHeight = 0.4f;
    private float armThickness = 0.2f;
    private float armLength = 0.8f;
    private float legLength = 0.8f;
    private float legThickness = 0.3f;
    private float legSeparation = 0.3f;
    private float headHeight = 0.5f;
    private float headThickness = 0.7f;
	
/**
 *  Constructor
 *  Initialize all the CubeRobot components
 */
    
    private BodyPart initializeBodyPart(Texture texture) {
    	Mesh mesh = new CubeMesh();
    	
    	ShaderProgram shader = new ShaderProgram(new Shader(GL_VERTEX_SHADER, VSHADER_FN), new Shader(GL_FRAGMENT_SHADER, FSHADER_FN), "colour");
    	shader.bindDataToShader("oc_position", mesh.vertex_handle, 3);
    	shader.bindDataToShader("oc_normal", mesh.normal_handle, 3);
    	shader.bindDataToShader("texcoord", mesh.tex_handle, 2);

    	Matrix4f transform = new Matrix4f();
    	
    	return new BodyPart(mesh, shader, texture, transform);
    }

    
    private BodyPart initializeBodyPart(String texturePath) {
    	Texture texture = new Texture();
    	texture.load(texturePath);
    	
    	return initializeBodyPart(texture);
    }
	public CubeRobot() {
		// Create body node
		
		// Initialise Geometry
		
//		Mesh body_mesh = new CubeMesh(); 
//		
//		ShaderProgram body_shader = new ShaderProgram(new Shader(GL_VERTEX_SHADER, VSHADER_FN), new Shader(GL_FRAGMENT_SHADER, FSHADER_FN), "colour");
//		body_shader.bindDataToShader("oc_position", body_mesh.vertex_handle, 3);
//		body_shader.bindDataToShader("oc_normal", body_mesh.normal_handle, 3);
//		body_shader.bindDataToShader("texcoord", body_mesh.tex_handle, 2);
//		
//		Texture body_texture = new Texture(); 
//		body_texture.load("resources/cubemap.png");
//		
//		Matrix4f body_transform = new Matrix4f(); 
//		
//		body = new BodyPart(body_mesh, body_shader, body_texture, body_transform);
		
		Texture armsLegsTexture = new Texture();
		armsLegsTexture.load("resources/cubemap_arms.png");
				
		body = initializeBodyPart("resources/cubemap_body.png");
		Matrix4f bodyTransform = body.getTransform();
		bodyTransform.scale(new Vector3f(bodyWidth, bodyHeight, bodyWidth));

		
		rightArm = initializeBodyPart(armsLegsTexture);
		Matrix4f rightArmTransform = rightArm.getTransform();
		rightArmTransform.translate(1, armHeight, 0);
		rightArmTransform.rotateAffineXYZ(0, 0, 0.2f);
		rightArmTransform.scale(armThickness, armLength, armThickness);
		rightArmTransform.translate(1, -1, 0);

		
		leftArm = initializeBodyPart(armsLegsTexture);
		Matrix4f leftArmTransform = leftArm.getTransform();
		leftArmTransform.translate(-1, armHeight, 0);
		leftArmTransform.rotateAffineXYZ(0, 0, -0.2f);
		leftArmTransform.scale(armThickness, armLength, armThickness);
		leftArmTransform.translate(-1, -1, 0);

		
		rightLeg = initializeBodyPart(armsLegsTexture);
		Matrix4f rightLegTransform = rightLeg.getTransform();
		rightLegTransform.translate(legThickness+legSeparation, -1-legLength, 0);
		rightLegTransform.scale(legThickness, legLength, legThickness);
		
		leftLeg = initializeBodyPart(armsLegsTexture);
		Matrix4f leftLegTransform = leftLeg.getTransform();
		leftLegTransform.translate(-legThickness-legSeparation, -1-legLength, 0);
		leftLegTransform.scale(legThickness, legLength, legThickness);

		
		head = initializeBodyPart("resources/cubemap_head_new.png");
		Matrix4f headTransform = head.getTransform();
		headTransform.translate(0, 1+headHeight, 0);
		headTransform.scale(headThickness, headHeight, headThickness);
		
		

		
		body.addChild(rightArm);
		body.addChild(leftArm);
		body.addChild(rightLeg);
		body.addChild(leftLeg);
		body.addChild(head);
		

	}
	

	/**
	 * Updates the scene and then renders the CubeRobot
	 * @param camera - Camera to be used for rendering
	 * @param deltaTime		- Time taken to render this frame in seconds (= 0 when the application is paused)
	 * @param elapsedTime	- Time elapsed since the beginning of this program in millisecs
	 */
	public void render(Camera camera, float deltaTime, long elapsedTime) {
		
		body.getTransform().rotateAffineXYZ(0, 0.3f*deltaTime, 0f);

		Matrix4f right_arm_transform = rightArm.getTransform();
		new Matrix4f().translate(1, armHeight, 0).rotateAffineXYZ(0, 0, (Math.floor(elapsedTime/2000) % 2 == 0 ? 1 : -1)*1.0f*deltaTime).translate(-1, -armHeight, 0).mul(right_arm_transform, right_arm_transform);
		
		
		//TODO: Render rest of the robot
		
		body.render(this, camera);
		
	}
	
	/**
	 * Draw mesh from a camera perspective
	 * @param camera		- Camera to be used for rendering
	 * @param mesh			- mesh to render
	 * @param modelMatrix	- model transformation matrix of this mesh
	 * @param shader		- shader to colour this mesh
	 * @param texture		- texture image to be used by the shader
	 */
	public void renderMesh(Camera camera, Mesh mesh , Matrix4f modelMatrix, ShaderProgram shader, Texture texture) {
		// If shaders modified on disk, reload them
		shader.reloadIfNeeded(); 
		shader.useProgram();

		// Step 2: Pass relevant data to the vertex shader
		
		// compute and upload MVP
		Matrix4f mvp_matrix = new Matrix4f(camera.getProjectionMatrix()).mul(camera.getViewMatrix()).mul(modelMatrix);
		shader.uploadMatrix4f(mvp_matrix, "mvp_matrix");
		
		// Upload Model Matrix and Camera Location to the shader for Phong Illumination
		shader.uploadMatrix4f(modelMatrix, "m_matrix");
		shader.uploadVector3f(camera.getCameraPosition(), "wc_camera_position");
		
		// Transformation by a nonorthogonal matrix does not preserve angles
		// Thus we need a separate transformation matrix for normals
		Matrix3f normal_matrix = new Matrix3f();
		modelMatrix.normal(normal_matrix);
		
		shader.uploadMatrix3f(normal_matrix, "normal_matrix");
		
		// Step 3: Draw our VertexArray as triangles
		// Bind Textures
		texture.bindTexture();
		shader.bindTextureToShader("tex", 0);
		skybox.bindCubemap();
		shader.bindTextureToShader("skybox", 1);
		// draw
		glBindVertexArray(mesh.vertexArrayObj); // Bind the existing VertexArray object
		glDrawElements(GL_TRIANGLES, mesh.no_of_triangles, GL_UNSIGNED_INT, 0); // Draw it as triangles
		glBindVertexArray(0);             // Remove the binding
		
        // Unbind texture
		texture.unBindTexture();
		skybox.unBindCubemap();
	}
}
