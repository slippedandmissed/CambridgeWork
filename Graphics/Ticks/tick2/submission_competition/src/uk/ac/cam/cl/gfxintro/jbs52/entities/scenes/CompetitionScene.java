package uk.ac.cam.cl.gfxintro.jbs52.entities.scenes;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import uk.ac.cam.cl.gfxintro.jbs52.entities.CubeRobot;
import uk.ac.cam.cl.gfxintro.jbs52.entities.Entity;
import uk.ac.cam.cl.gfxintro.jbs52.entities.TextEntity;
import uk.ac.cam.cl.gfxintro.jbs52.tick2.Camera;
import uk.ac.cam.cl.gfxintro.jbs52.tick2.CameraMotion;
import uk.ac.cam.cl.gfxintro.jbs52.tick2.SkyBox;

public class CompetitionScene extends Scene {

	private static final float TITLE_DURATION = 3;
	private static final float TITLE_TRANSITION_DEPTH = 10f;
	private static final float TITLE_TRANSITION_TIME = 1f;
	private static final float TITLE_TRANSITION_SPEED = TITLE_TRANSITION_DEPTH / TITLE_TRANSITION_TIME;
	private static final int ROW_COUNT = 8;
	private static final float CREW_SPACING = 6f;
	private static final float ROW_SPACING = 3f;
	private static final int FIRST_ROW_COUNT = 3;
	private static final String[] OTHER_PEOPLE = { "type1", "type1", "type1", "type1", "type1" };
	private static final float OTHER_PEOPLE_DEPTH = 30f;
	private static final float OTHER_PEOPLE_SPACING = 6f;

	public CompetitionScene(SkyBox skybox, Camera camera) {
		super(skybox, camera);
	}

	private boolean doTitleScreen = true;

	private Entity titleScreen;
	private TextEntity subtitle;
	private Entity room;
	private CubeRobot bones;
	private Entity crew;
	private TextEntity rattleEm;

	private List<CubeRobot> crewMembers;
	private List<CubeRobot> otherPeople;
	private List<Float> fleeRotations;
	private List<CameraMotion> cameraMotions;
	private float subtitleRotation = 0;
	private float titleTransition = 0;

	private Random rng;

	private float uniformBetween(float a, float b) {
		return a + (b - a) * rng.nextFloat();
	}

	public void populate() {
		rng = new Random();
		crewMembers = new ArrayList<CubeRobot>();
		otherPeople = new ArrayList<CubeRobot>();
		fleeRotations = new ArrayList<Float>();
		cameraMotions = new ArrayList<CameraMotion>();

		titleScreen = new Entity();
		TextEntity title = new TextEntity("Bones Malone");
		title.scale = 1.2f;
		title.initialize();
		title.getTransform().translate(0, 1f, -3);
		subtitle = new TextEntity("And The Skeleton Crew");
		subtitle.getTransform().translate(0, -1f, -3).rotateAffineXYZ(0, (float) Math.PI, 0);
		subtitle.initialize();

		titleScreen.addChild(title);
		titleScreen.addChild(subtitle);

		titleScreen.getTransform().translate(0, TITLE_TRANSITION_DEPTH + 5f, 0);

		addChild(titleScreen);

		room = new Entity();

		Entity floor = Entity.cube("ground/grass");
		floor.getTransform().translate(0, 0, 16).scale(64, 0.1f, 64);
		floor.setParent(room);

		bones = new CubeRobot("skeleton/body", "skeleton/arms_and_legs", "skeleton/arms_and_legs",
				"skeleton/arms_and_legs", "skeleton/arms_and_legs", "skeleton/head");
		bones.initialize();

		Entity bonesParent = new Entity();
		bonesParent.getTransform().translate(0, 2.6f, 0);
		bonesParent.setParent(room);
		bones.setParent(bonesParent);

		crew = new Entity();
		for (int i = 0; i < ROW_COUNT; i++) {
			float start = -CREW_SPACING * ((i + FIRST_ROW_COUNT - 1) / 2f);
			for (int j = 0; j < i + FIRST_ROW_COUNT; j++) {
				CubeRobot crewMember = new CubeRobot("crew/body", "crew/arms_and_legs", "crew/arms_and_legs",
						"crew/arms_and_legs", "crew/arms_and_legs", "crew/head");
				crewMember.getTransform().translate(start + j * CREW_SPACING, 0.8f + 2 * 0.6f, -i * ROW_SPACING);
				crewMember.bodyHeight = uniformBetween(0.75f, 0.85f);
				crewMember.legLength = uniformBetween(0.55f, 0.65f);
				crewMember.runSpeed = uniformBetween(3, 4);
				crewMember.initialize();
				crewMembers.add(crewMember);
				crew.addChild(crewMember);
			}
		}

		crew.getTransform().translate(0, 0, -5.0f);
		crew.setParent(room);

		addChild(room);

		rattleEm = new TextEntity("Rattle 'em, boys!");
		rattleEm.initialize();
		rattleEm.getTransform().translate(0, 3, 0);
		rattleEm.setParent(bonesParent);
		rattleEm.hide();

		float otherPeopleStartX = -(OTHER_PEOPLE.length - 1) * OTHER_PEOPLE_SPACING / 2f;
		for (int i = 0; i < OTHER_PEOPLE.length; i++) {
			String texPrefix = "other_people/" + OTHER_PEOPLE[i] + "/";
			CubeRobot otherPerson = new CubeRobot(texPrefix + "body", texPrefix + "arms", texPrefix + "arms",
					texPrefix + "legs", texPrefix + "legs", texPrefix + "head");

			otherPerson.getTransform()
					.translate(otherPeopleStartX + (i * OTHER_PEOPLE_SPACING), 1.5f + 2 * 1.2f, OTHER_PEOPLE_DEPTH)
					.rotateAffineXYZ(0, (float) Math.PI, 0);
			otherPerson.bodyHeight = uniformBetween(1.4f, 1.6f);
			otherPerson.legLength = uniformBetween(1.1f, 1.3f);
			otherPerson.bodyWidth = uniformBetween(1.3f, 1.5f);
			otherPerson.headHeight = uniformBetween(0.6f, 0.8f);
			otherPerson.headThickness = uniformBetween(0.8f, 1.0f);
			otherPerson.armLength = uniformBetween(1.1f, 1.3f);
			otherPerson.armThickness = uniformBetween(0.3f, 0.5f);
			otherPerson.armHeight = uniformBetween(1.3f, 1.5f);
			otherPerson.fleeing = true;
			otherPerson.runSpeed = uniformBetween(3, 4);
			otherPerson.initialize();
			fleeRotations.add(0f);
			otherPeople.add(otherPerson);
			room.addChild(otherPerson);
		}

		cameraMotions.add(new CameraMotion(getCamera(), (float) (Math.PI), 0.3f, 8, 1000, 1000));
		cameraMotions.add(new CameraMotion(getCamera(), (float) (2 * Math.PI), 0f, 8, 2500, 1000));
		cameraMotions.add(new CameraMotion(getCamera(), (float) (3 * Math.PI), 0.3f, 30, 8000, 2000));

		if (doTitleScreen) {
			room.hide();
		} else {
			titleScreen.hide();
		}

		getTransform().translate(0, doTitleScreen ? -TITLE_TRANSITION_DEPTH - 5f : -5f, -5f);
	}

	@Override
	public void animate(float deltaTime, long elapsedTime) {
		long sceneTime = doTitleScreen ? elapsedTime - ((long) ((TITLE_DURATION + TITLE_TRANSITION_TIME) * 1000))
				: elapsedTime;

		if (doTitleScreen) {
			if (elapsedTime >= (TITLE_DURATION + TITLE_TRANSITION_TIME) * 1000) {
				titleScreen.hide();
				room.unhide();
			}

			if (subtitleRotation < Math.PI) {
				float angle = 3.0f * deltaTime;
				subtitle.rotateAffineXYZ(0, (float) Math.min(angle, Math.PI - subtitleRotation), 0);
				subtitleRotation += angle;
			}

			if (elapsedTime > TITLE_DURATION * 1000) {
				if (titleTransition < TITLE_TRANSITION_DEPTH) {
					float dist = TITLE_TRANSITION_SPEED * deltaTime;
					getTransform().translate(0, Math.min(dist, TITLE_TRANSITION_DEPTH - titleTransition), 0);
					titleTransition += dist;
				}
			}
		}

		for (CameraMotion cameraMotion : cameraMotions) {
			cameraMotion.animate(sceneTime);
		}

		if (4000 <= sceneTime && sceneTime < 4900) {
			bones.rotateLeftArm(3 * deltaTime);
		}

		if (sceneTime > 5000) {
			rattleEm.unhide();
		}

		if (5750 < sceneTime) {
			bones.run(deltaTime);
			bones.getParent().translate(0, 0, bones.runSpeed * deltaTime);
		}

		if (7500 < sceneTime) {
			for (CubeRobot crewMember : crewMembers) {
				crewMember.run(deltaTime);
				crewMember.translate(0, 0, crewMember.runSpeed * deltaTime);
			}
		}

		if (8500 < sceneTime) {
			rattleEm.hide();
			for (int i = 0; i < otherPeople.size(); i++) {
				CubeRobot otherPerson = otherPeople.get(i);
				otherPerson.run(deltaTime);
				otherPerson.translate(0, 0, otherPerson.runSpeed * deltaTime);
				float angle = 1.0f * otherPerson.runSpeed * deltaTime;
				float currentAngle = fleeRotations.get(i);
				if (currentAngle < Math.PI) {
					otherPerson.rotateAffineXYZ(0, (float) Math.min(angle, Math.PI - currentAngle), 0);
					fleeRotations.set(i, currentAngle + angle);
				}

			}
		}
	}
}
