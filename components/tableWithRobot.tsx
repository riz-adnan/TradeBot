// components/TableWithRobot.tsx
import React, { useRef, useEffect } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Html, useGLTF, OrbitControls } from '@react-three/drei';
import { Mesh } from 'three';

function Table() {
  return (
    <mesh position={[0, -1, 0]}>
      <boxGeometry args={[4, 0.1, 2]} />
      <meshStandardMaterial color="brown" />
    </mesh>
  );
}

function Robot({ onFinish }: { onFinish: () => void }) {
  const { scene } = useGLTF('/models/robot_playground/scene.gltf');
  const ref = useRef<Mesh>(null);
  
  // Animation: Move the robot from behind the table and lay on top
  useEffect(() => {
    let timeout: NodeJS.Timeout;
    
    const animation = {
      position: [0, -0.5, -1.5],
      rotation: [0, 0, 0],
      progress: 0,
    };

    function animateRobot() {
      animation.progress += 0.01;
      if (animation.progress < 1) {
        ref.current!.position.z = -1.5 + 1.5 * animation.progress;
        ref.current!.position.y = -0.5 + 0.5 * animation.progress;
        ref.current!.rotation.x = Math.PI * animation.progress;
        requestAnimationFrame(animateRobot);
      } else {
        onFinish();
      }
    }

    timeout = setTimeout(() => {
      requestAnimationFrame(animateRobot);
    }, 1000);

    return () => clearTimeout(timeout);
  }, [onFinish]);

  return <primitive object={scene} ref={ref} />;
}

function HiMessage() {
  return (
    <Html position={[0, 0.5, 0]}>
      <div style={{ color: 'white', fontSize: '2rem', fontWeight: 'bold' }}>Hi!</div>
    </Html>
  );
}

export default function TableWithRobot() {
  const [showHi, setShowHi] = React.useState(false);

  return (
    <Canvas style={{ height: '500px', width: '100%' }}>
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 5]} intensity={1} />
      <Table />
      <Robot onFinish={() => setShowHi(true)} />
      {showHi && <HiMessage />}
      <OrbitControls />
    </Canvas>
  );
}
