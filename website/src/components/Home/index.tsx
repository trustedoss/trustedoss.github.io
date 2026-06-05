/**
 * trustedoss.dev Home Component
 * CC BY 4.0 · OpenChain KWG · haksungjang
 */

import React from 'react';

import Hero from './Hero';
import Roadmap from './Roadmap';
import Features from './Features';
import Showcase from './Showcase';
import WhyKwg from './WhyKwg';
import FinalCTA from './FinalCTA';

export default function Home() {
  return (
    <>
      <Hero />
      <main>
        <Roadmap />
        <Features />
        <Showcase />
        <WhyKwg />
        <FinalCTA />
      </main>
    </>
  );
}
