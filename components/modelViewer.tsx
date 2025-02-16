// components/AnimatedModel.tsx
import React, { Suspense, useRef, useEffect } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, useGLTF } from '@react-three/drei';
import { AnimationMixer, Group } from 'three';

interface AnimatedModelProps {
  url: string;
}

function AnimatedModel({ url }: AnimatedModelProps) {
  const { scene, animations } = useGLTF(url);
  const mixerRef = useRef<AnimationMixer | null>(null);
  const groupRef = useRef<Group>(null);

  // Initialize AnimationMixer
  useEffect(() => {
    if (animations.length) {
      mixerRef.current = new AnimationMixer(scene);
      animations.forEach((clip) => mixerRef.current?.clipAction(clip).play());
    }
    return () => {
      // Clean up the mixer on unmount
      mixerRef.current?.stopAllAction();
    };
  }, [animations, scene]);

  // Update the animation on each frame
  useFrame((state, delta) => {
    mixerRef.current?.update(delta);
  });

  return (
    <group ref={groupRef}>
      <primitive object={scene} />
    </group>
  );
}

export default function ModelViewer({ url }: AnimatedModelProps) {
  return (
    <Canvas
        style={{ height: '100%', width: '100%', position: 'relative', top: '8rem' }}
        camera={{ position: [0, 1, 3], rotation: [-0.2, 0, 0], fov: 75 }}
    >
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 5]} intensity={1} />
      <Suspense fallback={null}>
        <AnimatedModel url={url} />
      </Suspense>
      <OrbitControls />
    </Canvas>
  );
}