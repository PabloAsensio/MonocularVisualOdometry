import './style.css'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'
import * as dat from 'dat.gui'

import { createCar } from './vehicles/car.js'
import { createFrame } from './vehicles/frame'


/**
 * VARIABLES
 */
const _MAP_WIDTH = 100
const _MAP_HEIGHT = _MAP_WIDTH
const _CAR_SCALE = 0.01

// Loading
const textureLoader = new THREE.TextureLoader()
const normalTexture = textureLoader.load('/textures/AsphaltNormalMap.jpg')

// Debug
const gui = new dat.GUI()

// Canvas
const canvas = document.querySelector('canvas.webgl')

// Scene
const scene = new THREE.Scene()

/**
 * Meshes
 */

// Asphalt
const asphaltMesh = new THREE.Mesh(
    new THREE.PlaneGeometry(_MAP_WIDTH, _MAP_HEIGHT),
    new THREE.MeshStandardMaterial({
        // transparent: true,
        // opacity: 0.85,
        color: 0x3d3c3c,
        side: THREE.DoubleSide,
        normalMap: normalTexture,
        normalScale: new THREE.Vector2(0.5, 0.5),
    })
)

asphaltMesh.rotation.x = -Math.PI / 2
scene.add(asphaltMesh)


const asphalt = gui.addFolder('Asphalt')

const frame = createFrame(1241, 356, 1);
// frame.position.z = 1
frame.position.y = 1
scene.add(frame)

/**
 * Lights
 */
const hemiLight = new THREE.HemisphereLight(0x000000, 0x3d3c3c, 7); // Sun Light
hemiLight.position.set(10, 5, 10)
hemiLight.rotation.x = 1
hemiLight.rotation.y = 0
hemiLight.rotation.z = 0
hemiLight.castShadow = true
scene.add(hemiLight)

const hemiLightGui = gui.addFolder('Light')
const lightPosGui = hemiLightGui.addFolder('Position')
lightPosGui.add(hemiLight.position, 'x').min(-10).max(10).step(0.01)
lightPosGui.add(hemiLight.position, 'y').min(-10).max(10).step(0.01)
lightPosGui.add(hemiLight.position, 'z').min(-10).max(10).step(0.01)
const lightRotGui = hemiLightGui.addFolder('Rotation')
lightRotGui.add(hemiLight.rotation, 'x').min(-10).max(10).step(0.01)
lightRotGui.add(hemiLight.rotation, 'y').min(-10).max(10).step(0.01)
lightRotGui.add(hemiLight.rotation, 'z').min(-10).max(10).step(0.01)

/**
 * Sizes
 */
const sizes = {
    width: window.innerWidth,
    height: window.innerHeight
}

window.addEventListener('resize', () => {
    // Update sizes
    sizes.width = window.innerWidth
    sizes.height = window.innerHeight

    // Update camera
    camera.aspect = sizes.width / sizes.height
    camera.updateProjectionMatrix()

    // Update renderer
    renderer.setSize(sizes.width, sizes.height)
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
})


const axesHelper = new THREE.AxesHelper(10); // The X axis is red. The Y axis is green. The Z axis is blue.
scene.add(axesHelper);

/**
 * Camera
 */
// Base camera
const camera = new THREE.PerspectiveCamera(75, sizes.width / sizes.height, 0.1, 1000)
camera.position.x = -3
camera.position.y = 1.8
camera.position.z = 0
scene.add(camera)

const cameraGui = gui.addFolder('Camera')
const positionCameraGui = cameraGui.addFolder('Position')
positionCameraGui.add(camera.position, 'x').min(-5).max(10).step(0.01)
positionCameraGui.add(camera.position, 'y').min(-20).max(10).step(0.01)
positionCameraGui.add(camera.position, 'z').min(-5).max(10).step(0.01)

const rotationCameraGui = cameraGui.addFolder('Rotation')
rotationCameraGui.add(camera.rotation, 'x').min(-5).max(10).step(0.01)
rotationCameraGui.add(camera.rotation, 'y').min(-20).max(10).step(0.01)
rotationCameraGui.add(camera.rotation, 'z').min(-5).max(10).step(0.01)

// Controls
const controls = new OrbitControls(camera, canvas)
controls.enableDamping = true
// controls.enableKeys = true //older versions
controls.listenToKeyEvents(document.body)

/**
 * Renderer
 */
const renderer = new THREE.WebGLRenderer({
    canvas: canvas,
    antialias: true,
    alpha: true
})
// renderer.setFog(new THREE.FogExp2(0x000000, 0.1))
renderer.setSize(sizes.width, sizes.height)
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))

/**
 * Animate
 */

const tick = () => {

    frame.rotation.y += 0.005
    frame.position.x += 0.001
    frame.position.z += 0.001 * frame.position.x

    // Update Orbital Controls
    controls.target.copy(frame.position);
    controls.update()

    // Render
    renderer.render(scene, camera)

    // Call tick again on the next frame
    window.requestAnimationFrame(tick)
}

tick()