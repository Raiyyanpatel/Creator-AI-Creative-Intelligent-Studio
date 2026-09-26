import {
  GeneratedContent,
  GenerationInput,
  CopilotMessage,
  Scene,
} from "../types/creatorIntelligence";

export const mockGenerationService = {
  /**
   * Generates the initial comprehensive content plan from selected storyboard references.
   */
  generateInitialContent(input: GenerationInput): GeneratedContent {
    const isShort = input.contentType === "reel" || input.contentType === "short_video";
    const durationLabel = input.duration === "30_sec" ? "30s" : input.duration === "60_sec" ? "60s" : "90s";

    const defaultScenes: Scene[] = isShort
      ? [
          {
            id: "scene-1",
            sceneNumber: 1,
            duration: "0–3 sec",
            visual: "Creator holds phone directly to camera, screen glowing in low light. Quick whip-pan into lens.",
            dialogue: "Your phone is about to become smarter than most cloud AI workflows.",
            camera: "Close-up (35mm)",
            movement: "Fast snap push-in",
            bRollTrigger: "Smartphone silhouette macro",
          },
          {
            id: "scene-2",
            sceneNumber: 2,
            duration: "4–18 sec",
            visual: "Split screen showing Wi-Fi disabled with Airplane Mode on, while local 7B model executes 85 tokens/sec.",
            dialogue:
              "We just benchmarked local models on Snapdragon and Apple Neural Engine. Zero latency, zero cloud API bills, and 100% privacy.",
            camera: "Top-down desk probe view",
            movement: "Slow dynamic glide",
            bRollTrigger: "Live terminal token generation counter",
          },
          {
            id: "scene-3",
            sceneNumber: 3,
            duration: "19–30 sec",
            visual: "Creator smiles, tapping the back of phone. Kinetic text overlay appears with download link.",
            dialogue:
              "The future of AI is not in some massive data center. It's in your pocket. Drop a comment below to get the setup guide.",
            camera: "Medium shot (50mm)",
            movement: "Static eye-level lock",
            bRollTrigger: "Fast kinetic typography loop",
          },
        ]
      : [
          {
            id: "scene-1",
            sceneNumber: 1,
            duration: "0–15 sec",
            visual: "Moody cinematic lighting in creator studio. Creator looks directly into lens before looking down at laptop.",
            dialogue:
              "If you've been watching the AI boom over the last 18 months, you've probably noticed a quiet but massive shift happening beneath the surface.",
            camera: "Medium close-up",
            movement: "Slow steady push-in",
            bRollTrigger: "Server farm b-roll fading into microchip wafer",
          },
          {
            id: "scene-2",
            sceneNumber: 2,
            duration: "16–60 sec",
            visual: "Screen share demonstrating offline local Ollama model vs OpenAI cloud API roundtrip latency.",
            dialogue:
              "Today, we are examining concrete benchmarks. Look at this latency disparity: cloud calls took 1.4 seconds; local edge execution responded in 120 milliseconds.",
            camera: "Over-the-shoulder 4K screen capture",
            movement: "Pan across latency comparison graph",
            bRollTrigger: "High-contrast animated benchmark charts",
          },
          {
            id: "scene-3",
            sceneNumber: 3,
            duration: "61–90 sec",
            visual: "Creator standing by whiteboard outlining autonomous agent architecture and memory persistence.",
            dialogue:
              "When you couple on-device speed with autonomous tool protocols, the entire operating system transforms from passive software into an active collaborator.",
            camera: "Wide studio angle",
            movement: "Slow tracking lateral dolly",
            bRollTrigger: "Visual architectural flow diagram",
          },
        ];

    return {
      id: `gen-${Date.now()}`,
      title: "The Future of AI Is On Your Phone: Offline & Autonomous",
      hook: "Your phone is about to become smarter than most cloud AI workflows.",
      coreMessage:
        "On-device neural processing is reaching parity with cloud models, shifting the creator paradigm from subscription API reliance to private, zero-latency local execution.",
      script: defaultScenes.map((s) => `[${s.duration}] ${s.dialogue}`).join("\n\n"),
      scenes: defaultScenes,
      visualDirection: {
        camera: "Close-up / Medium shot with 35mm f/1.8 prime lens",
        movement: "Slow controlled push-in for focus; whip transitions between acts",
        lighting: "Cool cinematic studio with warm amber practical rim light",
        colorPalette: "Deep teal, matte carbon, and neon amber accent",
      },
      broll: [
        "Macro probe shot gliding across smartphone motherboard and silicon die",
        "Airplane mode toggle sequence showing Wi-Fi disabled with model still generating",
        "Terminal execution comparison showing live token latency meter",
        "Creator typing with natural studio depth of field",
      ],
      music: {
        genre: "Atmospheric Synthwave / Lo-Fi Electronic",
        bpm: 124,
        mood: "Focused, Futuristic, High Curiosity",
      },
      cta: "Try running your next creator workflow locally. Comment 'OFFLINE' for the repo.",
      targetPlatform: isShort ? "Instagram Reels & YouTube Shorts" : "YouTube Deep Dive",
      estimatedRetention: "78% watch-through rate projected based on 3-second hook velocity",
      changesApplied: ["✓ Initial synthesis from storyboard references"],
      version: 1,
    };
  },

  /**
   * Deterministic mock AI response engine that modifies the draft based on creator prompt.
   */
  processCopilotCommand(
    userCommand: string,
    currentDraft: GeneratedContent
  ): {
    responseMessage: CopilotMessage;
    updatedDraft: GeneratedContent;
  } {
    const cmd = userCommand.trim().toLowerCase();
    const updatedDraft: GeneratedContent = JSON.parse(JSON.stringify(currentDraft));
    updatedDraft.version += 1;

    let replyText = "";
    let changesMade: { field: string; before: string; after: string }[] = [];
    let appliedSummary = "";

    if (cmd.includes("controversial") || cmd.includes("spicy")) {
      const beforeHook = updatedDraft.hook;
      updatedDraft.hook = "Cloud AI is a scam for 90% of creators. Here is what big tech doesn't want you to know.";
      updatedDraft.coreMessage =
        "Massive cloud AI subscriptions are built to lock creators into recurring fees, while free open-source local models can already do 95% of the same creative tasks on your laptop and phone.";
      if (updatedDraft.scenes.length > 0) {
        updatedDraft.scenes[0].dialogue = updatedDraft.hook;
      }
      replyText = "Updated the hook and core message to challenge the mainstream SaaS consensus and provoke immediate comments.";
      changesMade = [
        {
          field: "Hook",
          before: beforeHook,
          after: updatedDraft.hook,
        },
        {
          field: "Core Thesis",
          before: "Balanced comparison between cloud and edge",
          after: "Provocative teardown of recurring cloud subscription models",
        },
      ];
      appliedSummary = "✓ Hook (Controversial) ✓ Core Thesis";
      updatedDraft.changesApplied = ["✓ Controversial Hook applied", "✓ High-dissonance thesis"];
    } else if (cmd.includes("shorter") || cmd.includes("punchier") || cmd.includes("brief")) {
      const beforeHook = updatedDraft.hook;
      updatedDraft.hook = "Cloud AI is dead. Your phone won.";
      if (updatedDraft.scenes.length > 0) {
        updatedDraft.scenes[0].dialogue = updatedDraft.hook;
      }
      replyText = "Tightened the opening hook to 6 words. Maximizes retention on fast mobile scroll feeds.";
      changesMade = [
        {
          field: "Hook",
          before: beforeHook,
          after: updatedDraft.hook,
        },
      ];
      appliedSummary = "✓ 6-Word Micro Hook";
      updatedDraft.changesApplied = ["✓ Hook shortened to 6 words"];
    } else if (cmd.includes("usual style") || cmd.includes("creator style") || cmd.includes("tone")) {
      const beforeScript = updatedDraft.scenes[0]?.dialogue || "";
      updatedDraft.hook = "नमस्कार दोस्तों! क्या आपने कभी सोचा है कि आपका फोन बिना इंटरनेट के इतना स्मार्ट कैसे हो सकता है?";
      if (updatedDraft.scenes.length > 0) {
        updatedDraft.scenes[0].dialogue = updatedDraft.hook;
      }
      updatedDraft.visualDirection.camera = "Direct eye-level 50mm pedagogical framing with deliberate 1.2s micro-pauses";
      replyText = "Injected your signature vocal architecture: conversational bilingual greeting, inclusive plural pronouns ('we are exploring'), and calculated micro-pauses before data reveals.";
      changesMade = [
        {
          field: "Vocal Architecture",
          before: beforeScript,
          after: updatedDraft.hook,
        },
        {
          field: "Pacing Dynamics",
          before: "Standard rapid delivery",
          after: "Pedagogical Hindi/English mix with 1.2s pause before evidence",
        },
      ];
      appliedSummary = "✓ Native Linguistic Style ✓ Micro-Pause Pacing";
      updatedDraft.changesApplied = ["✓ Signature Creator Style & Hindi Cadence"];
    } else if (cmd.includes("cinematic") || cmd.includes("visual") || cmd.includes("camera")) {
      updatedDraft.visualDirection = {
        camera: "Anamorphic 2.39:1 widescreen, 35mm T2.0 lens with blue streak flares",
        movement: "Slow mechanical motion-control push-in combined with 120fps high-speed B-roll",
        lighting: "Moody cyberpunk split lighting: 3200K tungsten key with deep cyan edge rim",
        colorPalette: "Kodak Vision3 500T film simulation with subtle halation",
      };
      if (updatedDraft.scenes.length > 1) {
        const beforeScene2 = updatedDraft.scenes[1].visual;
        updatedDraft.scenes[1].visual =
          "Extreme macro probe lens gliding 2mm above the silicon chip with holographic animated neural pathways pulsing in sync with music.";
        changesMade.push({
          field: "Scene 2 Visual",
          before: beforeScene2,
          after: updatedDraft.scenes[1].visual,
        });
      }
      replyText = "Elevated the visual direction to cinema-grade production with anamorphic lens specs, moody tungsten/cyan split lighting, and macro probe b-roll.";
      changesMade.push({
        field: "Visual Direction",
        before: "Standard studio lighting",
        after: "2.39:1 Anamorphic, cyan rim, macro probe lens gliding over silicon",
      });
      appliedSummary = "✓ Anamorphic Visuals ✓ Macro Probe Lighting";
      updatedDraft.changesApplied = ["✓ Cinematic Lens & Lighting Direction"];
    } else if (cmd.includes("cta") || cmd.includes("call to action")) {
      const beforeCta = updatedDraft.cta;
      updatedDraft.cta = "Comment 'OFFLINE' right now and I'll DM you my exact 3-step setup script + model weights link.";
      replyText = "Swapped the generic ending with an algorithmic keyword trigger CTA. Increases comment velocity by up to 300%.";
      changesMade = [
        {
          field: "Closing CTA",
          before: beforeCta,
          after: updatedDraft.cta,
        },
      ];
      appliedSummary = "✓ High-Converting Comment Trigger CTA";
      updatedDraft.changesApplied = ["✓ High-Velocity Comment CTA"];
    } else if (cmd.includes("reel") || cmd.includes("30") || cmd.includes("short")) {
      updatedDraft.targetPlatform = "Instagram Reels & YouTube Shorts";
      updatedDraft.scenes = [
        {
          id: "s1",
          sceneNumber: 1,
          duration: "0–3 sec",
          visual: "Creator abruptly turns off airplane mode on screen, smiles knowingly at camera.",
          dialogue: "Cloud AI is dead. Your phone just replaced it.",
          camera: "Vertical 9:16 tight crop",
          movement: "Handheld kinetic shake",
        },
        {
          id: "s2",
          sceneNumber: 2,
          duration: "4–20 sec",
          visual: "Rapid 3-beat montage: 1) Model answering offline, 2) Zero battery drain, 3) 100% private data.",
          dialogue: "Offline 7B models run at 85 tokens per second. Zero lag. Zero monthly subscriptions.",
          camera: "Over-the-shoulder screen macro",
          movement: "Whip pans between beats",
        },
        {
          id: "s3",
          sceneNumber: 3,
          duration: "21–30 sec",
          visual: "Seamless loop back to opening gesture, pointing down to comment section.",
          dialogue: "Comment 'LOCAL' and I'll send you the free download link.",
          camera: "Close-up eye contact",
          movement: "Snap zoom out",
        },
      ];
      replyText = "Restructured the entire script into a 30-second hyper-kinetic vertical Reel with a seamless replay loop.";
      changesMade = [
        {
          field: "Format & Duration",
          before: "Horizontal video structure",
          after: "30-second vertical 9:16 three-beat loop structure",
        },
      ];
      appliedSummary = "✓ 30s Reel Format ✓ Seamless Loop";
      updatedDraft.changesApplied = ["✓ 30-second Reel format with seamless loop"];
    } else {
      // Intelligent general response
      replyText = `Understood! I refined the content draft to emphasize ${userCommand.replace(/[?.!]/g, "")}, sharpening the contrast in the opening scenes and elevating the production clarity.`;
      changesMade = [
        {
          field: "Content Polish",
          before: "Draft v" + currentDraft.version,
          after: "Refined with focus on: " + userCommand,
        },
      ];
      appliedSummary = "✓ Creative Refinement Applied";
      updatedDraft.changesApplied = ["✓ Refined based on feedback: " + userCommand];
    }

    // Refresh script field from updated scenes
    updatedDraft.script = updatedDraft.scenes.map((s) => `[${s.duration}] ${s.dialogue}`).join("\n\n");

    const responseMessage: CopilotMessage = {
      id: `msg-${Date.now()}`,
      sender: "ai",
      text: replyText,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      changesMade,
      appliedSummary,
    };

    return {
      responseMessage,
      updatedDraft,
    };
  },
};
