import React, { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { useGLTF } from '@react-three/drei';
import { Vector3 } from 'three';

// Defining the bull head props
interface BullHeadProps {
    url: string;
}

function BullHead({ url }: BullHeadProps) {
    const modelRef = useRef<any>();
    const mouse = useRef(new Vector3());

    // Load the GLTF model
    const { scene } = useGLTF(url) as any;

    // Update the model's rotation to follow the cursor
    useFrame(({ mouse: { x, y }, camera }) => {
        const vec = new Vector3(x, y, 0).unproject(camera);
        vec.sub(camera.position).normalize();

        mouse.current.x = (x * 0.3) * Math.PI;
        mouse.current.y = (y * 0.3) * Math.PI;

        if (modelRef.current) {
            modelRef.current.rotation.y = mouse.current.x;
            modelRef.current.rotation.x = -mouse.current.y;
        }
    });

    return <primitive ref={modelRef} object={scene} />;
};

export default function BullHeadCanvas({ url }: BullHeadProps) {
    return (
        <Canvas
            style={{ height: '50vh', width: '96vw', position: 'relative', top: '-1rem', left: '-10rem', zIndex: 20 }}
            camera={{ position: [0, 0, 1], rotation: [0, 0, 0], fov: 75 }}
        >
            <ambientLight intensity={0.5} />
            <directionalLight position={[0, 0, 5]} />
            <BullHead url={url} />
        </Canvas>
    );
};