package uk.ac.cam.cl.gfxintro.jbs52.entities;

import org.joml.Matrix4f;
import org.joml.Vector3f;

import uk.ac.cam.cl.gfxintro.jbs52.entities.scenes.Scene;
import uk.ac.cam.cl.gfxintro.jbs52.tick2.Camera;
import uk.ac.cam.cl.gfxintro.jbs52.tick2.SkyBox;;

public class CubeRobot extends Entity {

	// Components of this CubeRobot

	private Entity body;
	private Entity rightArm;
	private Entity leftArm;
	private Entity rightLeg;
	private Entity leftLeg;
	private Entity head;

	public float bodyHeight = 1.0f;
	public float bodyWidth = 1.0f;
	public float armHeight = 0.4f;
	public float armThickness = 0.2f;
	public float armLength = 0.8f;
	public float legLength = 0.8f;
	public float legWidth = 0.3f;
	public float legSeparation = 0.3f;
	public float headHeight = 0.5f;
	public float headThickness = 0.7f;
	public float initialArmAngle = 0.2f;
	public float runSpeed = 5f;
	public float adjustSpeed = 9f;
	public float legAngleExtremity = 1;
	public float armAngleExtremity = 1;
	public float headBobExtremity = 0.2f;
	public float fleeingArmAngle = 2.5f;
	public float fleeingArmExtremity = 0.2f;
	public boolean fleeing = false;

	private float rightArmAngle;
	private float leftArmAngle;
	private float rightLegAngle;
	private float leftLegAngle;
	private float headElevation;

	private boolean running = false;
	private int rightArmSwingDirection = 1;
	private int leftArmSwingDirection = 1;
	private int rightLegSwingDirection = 1;
	private int leftLegSwingDirection = 1;
	private int headBobDirection = 1;

	private static float clampAngle(float angle) {
		angle = (angle + (float) Math.PI) % (2f * (float) Math.PI);
		if (angle < 0) {
			angle += 2 * Math.PI;
		}
		return angle - (float) Math.PI;
	}

	/**
	 * Constructor Initialize all the CubeRobot components
	 */

	public CubeRobot(String bodyTex, String rightArmTex, String leftArmTex, String rightLegTex, String leftLegTex,
			String headTex) {

		body = Entity.cube(bodyTex);
		rightArm = Entity.cube(rightArmTex);
		leftArm = Entity.cube(leftArmTex);
		rightLeg = Entity.cube(rightLegTex);
		leftLeg = Entity.cube(leftLegTex);
		head = Entity.cube(headTex);
	}

	public void initialize() {
		rightArmAngle = initialArmAngle;
		leftArmAngle = initialArmAngle;
		rightLegAngle = 0;
		leftLegAngle = 0;
		headElevation = 0;

		Matrix4f bodyTransform = body.getTransform();
		bodyTransform.scale(new Vector3f(bodyWidth, bodyHeight, bodyWidth));

		Matrix4f rightArmTransform = rightArm.getTransform();
		rightArmTransform.translate(-bodyWidth, armHeight, 0);
		rightArmTransform.rotateAffineXYZ(0, 0, -initialArmAngle);
		rightArmTransform.scale(armThickness, armLength, armThickness);
		rightArmTransform.translate(-1, -1, 0);

		Matrix4f leftArmTransform = leftArm.getTransform();
		leftArmTransform.translate(bodyWidth, armHeight, 0);
		leftArmTransform.rotateAffineXYZ(0, 0, initialArmAngle);
		leftArmTransform.scale(armThickness, armLength, armThickness);
		leftArmTransform.translate(1, -1, 0);

		Matrix4f rightLegTransform = rightLeg.getTransform();
		rightLegTransform.translate(-legWidth - legSeparation, -bodyHeight - legLength, 0);
		rightLegTransform.scale(legWidth, legLength, legWidth);

		Matrix4f leftLegTransform = leftLeg.getTransform();
		leftLegTransform.translate(legWidth + legSeparation, -bodyHeight - legLength, 0);
		leftLegTransform.scale(legWidth, legLength, legWidth);

		Matrix4f headTransform = head.getTransform();
		headTransform.translate(0, bodyHeight + headHeight, 0);
		headTransform.scale(headThickness, headHeight, headThickness);

		this.addChild(body);
		this.addChild(rightArm);
		this.addChild(leftArm);
		this.addChild(rightLeg);
		this.addChild(leftLeg);
		this.addChild(head);
	}

	public Entity getHead() {
		return head;
	}

	public Entity getBody() {
		return body;
	}

	public Entity getRightArm() {
		return rightArm;
	}

	public Entity getLeftArm() {
		return leftArm;
	}

	public Entity getRightLeg() {
		return rightLeg;
	}

	public Entity getLeftLeg() {
		return leftLeg;
	}

	public float getRightArmAngle() {
		return rightArmAngle;
	}

	public float getLeftArmAngle() {
		return leftArmAngle;
	}

	public float getRightLegAngle() {
		return rightLegAngle;
	}

	public float getLeftLegAngle() {
		return leftLegAngle;
	}

	public void rotateRightArm(float angle) {
		Matrix4f rightArmTransform = rightArm.getTransform();
		new Matrix4f().translate(-bodyWidth, armHeight, 0).rotateAffineXYZ(0, 0, -angle)
				.translate(bodyWidth, -armHeight, 0).mul(rightArmTransform, rightArmTransform);
		rightArmAngle = clampAngle(rightArmAngle + angle);
	}

	public void rotateLeftArm(float angle) {
		Matrix4f leftArmTransform = leftArm.getTransform();
		new Matrix4f().translate(bodyWidth, armHeight, 0).rotateAffineXYZ(0, 0, angle)
				.translate(-bodyWidth, -armHeight, 0).mul(leftArmTransform, leftArmTransform);
		leftArmAngle = clampAngle(leftArmAngle + angle);
	}

	public void rotateRightLeg(float angle) {
		Matrix4f rightLegTransform = rightLeg.getTransform();
		new Matrix4f().translate(-legWidth - legSeparation, -bodyHeight, -legWidth).rotateAffineXYZ(-angle, 0, 0)
				.translate(legWidth + legSeparation, bodyHeight, legWidth).mul(rightLegTransform, rightLegTransform);
		rightLegAngle = clampAngle(rightLegAngle + angle);
	}

	public void rotateLeftLeg(float angle) {
		Matrix4f leftLegTransform = leftLeg.getTransform();
		new Matrix4f().translate(legWidth + legSeparation, -bodyHeight, -legWidth).rotateAffineXYZ(-angle, 0, 0)
				.translate(-legWidth - legSeparation, bodyHeight, legWidth).mul(leftLegTransform, leftLegTransform);
		leftLegAngle = clampAngle(leftLegAngle + angle);
	}

	public void raiseHead(float dist) {
		Matrix4f headTransform = head.getTransform();
		new Matrix4f().translate(0, dist, 0).mul(headTransform, headTransform);
		headElevation += dist;
	}

	public void setRightArmAngle(float angle) {
		rotateRightArm(angle - rightArmAngle);
	}

	public void setLeftArmAngle(float angle) {
		rotateLeftArm(angle - leftArmAngle);
	}

	public void setRightLegAngle(float angle) {
		rotateRightLeg(angle - rightLegAngle);
	}

	public void setLeftLegAngle(float angle) {
		rotateLeftLeg(angle - leftLegAngle);
	}

	private float getCorrectionAngle(float error, float step) {
		return -Math.signum(error) * Math.min(Math.abs(error), step);
	}

	private static boolean approxZero(float x) {
		float error = 0.00001f;
		return -error < x && x < error;
	}

	public void run(float deltaTime) {
		if (running) {
			float legStep = runSpeed * deltaTime;
			float armStep = legStep * armAngleExtremity / legAngleExtremity / 2;
			float headStep = legStep * headBobExtremity / legAngleExtremity / 2;

			if (fleeing) {
				rotateRightArm(rightArmSwingDirection * armStep);
				if (rightArmSwingDirection * (rightArmAngle - fleeingArmAngle) >= fleeingArmExtremity) {
					rightArmSwingDirection *= -1;
				}

				rotateLeftArm(leftArmSwingDirection * armStep);
				if (leftArmSwingDirection * (leftArmAngle - fleeingArmAngle) >= fleeingArmExtremity) {
					leftArmSwingDirection *= -1;
				}
			} else {

				rotateRightArm(rightArmSwingDirection * armStep);
				if (rightArmSwingDirection
						* rightArmAngle >= (armAngleExtremity + rightArmSwingDirection * armAngleExtremity) / 2) {
					rightArmSwingDirection *= -1;
				}

				rotateLeftArm(leftArmSwingDirection * armStep);
				if (leftArmSwingDirection
						* leftArmAngle >= (armAngleExtremity + leftArmSwingDirection * armAngleExtremity) / 2) {
					leftArmSwingDirection *= -1;
				}
			}

			rotateRightLeg(rightLegSwingDirection * legStep);
			if (rightLegSwingDirection * rightLegAngle >= legAngleExtremity) {
				rightLegSwingDirection *= -1;
			}

			rotateLeftLeg(leftLegSwingDirection * legStep);
			if (leftLegSwingDirection * leftLegAngle >= legAngleExtremity) {
				leftLegSwingDirection *= -1;
			}

			raiseHead(headBobDirection * headStep);
			if (headBobDirection * headElevation >= (headBobExtremity + headBobDirection * headBobExtremity) / 2) {
				headBobDirection *= -1;
			}
		} else {
			float legStep = adjustSpeed * deltaTime;
			float armStep = legStep * armAngleExtremity / legAngleExtremity / 2;
			float headStep = legStep * headBobExtremity / legAngleExtremity / 2;

			if (fleeing) {
				rotateRightArm(getCorrectionAngle(rightArmAngle - fleeingArmAngle, armStep));
				rotateLeftArm(getCorrectionAngle(leftArmAngle - fleeingArmAngle, armStep));
			} else {
				rotateRightArm(getCorrectionAngle(rightArmAngle, armStep));
				rotateLeftArm(getCorrectionAngle(leftArmAngle - armAngleExtremity, armStep));
			}
			rotateRightLeg(getCorrectionAngle(rightLegAngle - legAngleExtremity, legStep));
			rotateLeftLeg(getCorrectionAngle(leftLegAngle, legStep));
			raiseHead(getCorrectionAngle(headElevation, headStep));

			if ((fleeing || (approxZero(rightArmAngle) && approxZero(leftArmAngle - armAngleExtremity)))
					&& approxZero(rightLegAngle - legAngleExtremity) && approxZero(leftLegAngle)
					&& approxZero(headElevation)) {
				running = true;
			}
		}
	}

	public void stopRunning() {
		running = false;
	}

}
