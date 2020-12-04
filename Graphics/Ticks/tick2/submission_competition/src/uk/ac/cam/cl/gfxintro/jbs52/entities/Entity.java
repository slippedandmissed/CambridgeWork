package uk.ac.cam.cl.gfxintro.jbs52.entities;

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
import org.joml.Vector3f;

import uk.ac.cam.cl.gfxintro.jbs52.tick2.Camera;
import uk.ac.cam.cl.gfxintro.jbs52.tick2.CubeMesh;
import uk.ac.cam.cl.gfxintro.jbs52.tick2.Mesh;
import uk.ac.cam.cl.gfxintro.jbs52.tick2.Shader;
import uk.ac.cam.cl.gfxintro.jbs52.tick2.ShaderProgram;
import uk.ac.cam.cl.gfxintro.jbs52.tick2.SkyBox;
import uk.ac.cam.cl.gfxintro.jbs52.tick2.Texture;
import uk.ac.cam.cl.gfxintro.jbs52.tick2.TextureCache;

public class Entity {

	private final static String VSHADER_FN = "resources/cube_vertex_shader.glsl";
	private final static String FSHADER_FN = "resources/cube_fragment_shader.glsl";

	private Mesh mesh;
	private ShaderProgram shader;
	private Texture texture;
	private Matrix4f transform;

	private Entity parent;
	private List<Entity> children;

	private boolean hidden = false;

	public Entity() {
		transform = new Matrix4f();
		children = new ArrayList<Entity>();
	}

	public boolean isHidden() {
		return hidden;
	}

	public void setHidden(boolean hidden) {
		this.hidden = hidden;
	}

	public void hide() {
		setHidden(true);
	}

	public void unhide() {
		setHidden(false);
	}

	public void setParent(Entity parent) {
		this.unsetParent();
		this.parent = parent;
		parent.children.add(this);
	}

	public void unsetParent() {
		if (this.parent != null) {
			this.parent.children.remove(this);
			this.parent = null;
		}
	}

	public Entity getParent() {
		return parent;
	}

	public void addChild(Entity child) {
		child.setParent(this);
		children.add(child);
	}

	public static Entity cube(String texturePath) {
		return cube(TextureCache.get(texturePath));
	}

	public static Entity cube(Texture texture) {
		Mesh mesh = new CubeMesh();

		ShaderProgram shader = new ShaderProgram(new Shader(GL_VERTEX_SHADER, VSHADER_FN),
				new Shader(GL_FRAGMENT_SHADER, FSHADER_FN), "colour");
		shader.bindDataToShader("oc_position", mesh.vertex_handle, 3);
		shader.bindDataToShader("oc_normal", mesh.normal_handle, 3);
		shader.bindDataToShader("texcoord", mesh.tex_handle, 2);

		Entity entity = new Entity();
		entity.mesh = mesh;
		entity.shader = shader;
		entity.texture = texture;

		return entity;
	}

	/**
	 * Draw mesh from a camera perspective
	 * 
	 * @param camera      - Camera to be used for rendering
	 * @param mesh        - mesh to render
	 * @param modelMatrix - model transformation matrix of this mesh
	 * @param shader      - shader to colour this mesh
	 * @param texture     - texture image to be used by the shader
	 */
	public void renderMesh(SkyBox skybox, Camera camera, Mesh mesh, Matrix4f modelMatrix, ShaderProgram shader,
			Texture texture) {
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
		glBindVertexArray(0); // Remove the binding

		// Unbind texture
		texture.unBindTexture();
		skybox.unBindCubemap();
	}

	public Matrix4f getTransform() {
		return transform;
	}

	public Matrix4f getLinkedTransform() {
		Matrix4f result = new Matrix4f(transform);
		Entity current = parent;
		while (current != null) {
			current.transform.mul(result, result);
			current = current.parent;
		}
		return result;
	}

	public void render(SkyBox skybox, Camera camera, float deltaTime, long elapsedTime) {
		render(skybox, getLinkedTransform(), camera, deltaTime, elapsedTime);
	}

	public void animate(float deltaTime, long elapsedTime) {

	}

	public void render(SkyBox skybox, Matrix4f linkedTransform, Camera camera, float deltaTime, long elapsedTime) {
		animate(deltaTime, elapsedTime);
		if (!hidden) {
			if (mesh != null) {
				renderMesh(skybox, camera, mesh, linkedTransform, shader, texture);
			}
			for (Entity child : children) {
				child.render(skybox, new Matrix4f(linkedTransform).mul(child.transform), camera, deltaTime,
						elapsedTime);
			}
		}
	}

	public void translate(float x, float y, float z) {
		new Matrix4f().translate(x, y, z).mul(transform, transform);
	}

	public void rotateAffineXYZ(float x, float y, float z) {
		Vector3f translation = new Vector3f();
		transform.getTranslation(translation);
		new Matrix4f().translate(translation).rotateAffineXYZ(x, y, z).translate(new Vector3f(translation).mul(-1))
				.mul(transform, transform);
	}

	public void scale(float x, float y, float z) {
		new Matrix4f().scale(x, y, z).mul(transform, transform);
	}

}
