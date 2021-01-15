let camera, scene, renderer, controls;
let particleSystem, particles, maxParticles;

initiate();
animate();

function initiate() {

    // Scene //
    scene = new THREE.Scene();
    scene.fog = new THREE.Fog(0x111111, 1, 200)

    // Camera //
    camera = new THREE.PerspectiveCamera( 60, window.innerWidth / window.innerHeight, 0.1, 1000 );
    camera.position.z = 2;

    // Light //
    const light = new THREE.HemisphereLight(0xffffff, 0x444444);
    light.position.set(0, 20, 0);
    scene.add(light);

    // Objects //
    let textLoader = new THREE.TextureLoader();
    let objLoader = new THREE.ObjectLoader();

    // -- Floor -- //
    const floorTexture = textLoader.load( "textures/snow-texture.jpg" );
    floorTexture.wrapS = floorTexture.wrapT = THREE.RepeatWrapping;
    floorTexture.repeat.set( 100, 100);
    floorTexture.anisotropy = 8;
    floorTexture.encoding = THREE.sRGBEncoding;
    const floorMaterial = new THREE.MeshPhongMaterial( { map: floorTexture, side: THREE.DoubleSide } );
    const floor = new THREE.Mesh(new THREE.PlaneBufferGeometry(200, 200), floorMaterial);
    floor.position.y = -2
    floor.rotation.x = Math.PI / 2;
    floor.receiveShadow = true;
    scene.add(floor);

    // -- Sky -- //
    const skyTexture = textLoader.load("textures/sky-texture.jpg");
    const skyMaterial = new THREE.MeshBasicMaterial( { map: skyTexture } );
    skyMaterial.side = THREE.BackSide;
    const sky = new THREE.Mesh(new THREE.SphereGeometry(100, 32, 15), skyMaterial);
    scene.add(sky)

    // -- Tree -- //
    objLoader.load("/models/Tree.obj", function(tree) {
        tree.position.x = 10;
        tree.position.y = 10;
        tree.position.z = -10;
        tree.scale.x = tree.scale.y = tree.scale.z = 2.0;
        scene.add(tree);
    });

    // -- Snow particles -- //
    maxParticles = 5000;

    particles = new THREE.Geometry;
    for (let i = 0; i <= maxParticles; i++){
        let particleX = Math.random() * 200 - 100,
            particleY = Math.random() * 200,
            particleZ = Math.random() * 200 - 100,
            particle = new THREE.Vector3(particleX, particleY, particleZ);
        particle.velocity = {};
        particle.velocity.y = 0;
        particles.vertices.push(particle);
    }

    const snowTexture = textLoader.load("textures/snow-particle-texture.png");
    const particleMaterial = new THREE.PointCloudMaterial({
    color: 0xffffff,
    map: snowTexture,
    transparent: true
    });

    particleSystem = new THREE.ParticleSystem(particles, particleMaterial);
    particleSystem.sortParticles = true;
    scene.add(particleSystem);

    // Controls //
    controls = new THREE.OrbitControls( camera );
    controls.addEventListener( 'change', render );

    // Renderer //
    renderer = new THREE.WebGLRenderer();
    renderer.setSize( window.innerWidth, window.innerHeight );
    document.body.appendChild( renderer.domElement );
}

// Simulates falling snow //
function snow() {
    let count = maxParticles;
    while(count--){
        let particle = particles.vertices[count];
        if(particle.y < 0){
            particle.y = 100;
            particle.velocity.y = 0;
            particle.z = Math.random() * 200 - 100;
            particle.velocity.z = 0
        }
        particle.velocity.y -= Math.random() * 0.01;
        particle.y += particle.velocity.y;
        particle.velocity.z += Math.random() * 0.002;
        particle.z += particle.velocity.z;
    }
    particles.verticesNeedUpdate = true;
}

function animate() {
    requestAnimationFrame( animate );
    snow();
    render();
}

function render() {
    renderer.render( scene, camera );
}



