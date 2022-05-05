import './style.css'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'

import { createFrame } from './vehicles/frame'
require('./utils/CBuffer.js')

async function decode_utf8(s) {
    return decodeURIComponent(escape(s));
}

/**
 * VARIABLES
 */
const _MAP_WIDTH = 100
const _MAP_HEIGHT = _MAP_WIDTH
const ARRAY_LENGHT = 300


// Loading
const textureLoader = new THREE.TextureLoader()
const normalTexture = textureLoader.load('/textures/AsphaltNormalMap.jpg')

// Canvas
const canvas = document.querySelector('canvas.webgl')

// Scene
const scene = new THREE.Scene()

/**
 * Grid
 */
const grid = new THREE.GridHelper(1000, 100, 0x888888, 0x888888);
grid.position.set(0, -0.1, 0);
scene.add(grid);

/**
 * Frame
 */
const frame = createFrame(1241, 356, 1, 0x00ff00);
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

const axesHelper = new THREE.AxesHelper(8); // The X axis is red. The Y axis is green. The Z axis is blue.
scene.add(axesHelper);

/**
 * Camera
 */
// Base camera
const camera = new THREE.PerspectiveCamera(75, sizes.width / sizes.height, 0.1, 1000)
camera.position.x = -30
camera.position.y = 18
camera.position.z = -10
scene.add(camera)

// Controls
const controls = new OrbitControls(camera, canvas)
controls.enableDamping = true
controls.listenToKeyEvents(document.body)

/**
 * Renderer
 */
const renderer = new THREE.WebGLRenderer({
    canvas: canvas,
    antialias: true,
    alpha: true
})
renderer.setSize(sizes.width, sizes.height)
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))

/**
 * Tracker
 */
function createTrack(track, color = 0xff0000) {
    const material = new THREE.LineBasicMaterial({ color: color, linewidth: 2 });
    const geometry = new THREE.BufferGeometry().setFromPoints(track.getPoints());
    const line = new THREE.Line(geometry, material);
    return line
}

/**
 * Animate
 */
let track = []
let image_canvas = document.getElementById('image');
const tracker = new CBuffer(ARRAY_LENGHT)

const socket = new WebSocket('ws://localhost:7890');
socket.onopen = function (event) {
    console.log('Connected to server');
    socket.send("run");
};
socket.onmessage = async function (event) {
    let data = JSON.parse(event.data);
    frame.position.x = data.pose.x * .1
    frame.position.y = data.pose.y * .1
    frame.position.z = data.pose.z * .1

    tracker.push(frame.position.clone())

    if (!(track === [])) {
        scene.remove(track)
        track = createTrack(tracker)
        scene.add(track)
    }

    // Parse Image Data
    var image_data = data.img_data,
        source = await decode_utf8(image_data.image),
        shape = image_data.shape;

    image_canvas.src = 'data:image/jpeg;base64,' + source;
    image_canvas.width = shape[1];
    image_canvas.height = shape[0];

};
socket.onclose = async function (event) {
    console.log('Connection closed');
};


const tick = () => {
    // Update Orbital Controls
    controls.update()

    // Render
    renderer.render(scene, camera)

    // Call tick again on the next frame
    window.requestAnimationFrame(tick)
}

tick()