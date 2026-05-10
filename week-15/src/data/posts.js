export const categories = [
  "All",
  "Technology",
  "Design",
  "Science",
  "Travel",
  "Lifestyle",
  "Business",
];

export const posts = [
  {
    id: 1,
    title: "The Future of AI: What to Expect in 2026",
    slug: "future-of-ai-2026",
    category: "Technology",
    author: "Alex Chen",
    authorAvatar: "AC",
    date: "2026-05-01",
    readTime: "6 min read",
    excerpt:
      "Artificial intelligence is reshaping every industry. From generative models to autonomous agents, the pace of innovation has never been faster.",
    content: `Artificial intelligence is reshaping every industry. From generative models to autonomous agents, the pace of innovation has never been faster. In 2026, we're witnessing a convergence of large language models, multimodal AI, and real-time inference that seemed impossible just three years ago.

## The Rise of Agentic AI

Agents capable of browsing the web, writing code, and executing multi-step tasks are now mainstream. Tools like Claude, GPT-4o, and Gemini Ultra operate with unprecedented autonomy. Enterprises are deploying fleets of AI workers to handle customer support, data analysis, and software development.

## Multimodal Breakthroughs

Vision-language models have matured to the point where they can analyze medical images with radiologist-level accuracy. Real-time video understanding enables applications from autonomous vehicles to live sports analytics.

## What This Means for Developers

For software engineers, AI is both a tool and a challenge. Learning to work alongside AI systems — understanding their limitations, guiding their outputs, and integrating them into products — is the most valuable skill of the decade.

The future belongs to those who can bridge human creativity with machine intelligence.`,
    tags: ["AI", "Machine Learning", "Future Tech"],
    coverGradient: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
  },
  {
    id: 2,
    title: "Design Systems That Scale: Lessons from Big Tech",
    slug: "design-systems-that-scale",
    category: "Design",
    author: "Maya Patel",
    authorAvatar: "MP",
    date: "2026-04-28",
    readTime: "8 min read",
    excerpt:
      "Building a design system is one thing. Making it scale across hundreds of teams and thousands of components is an entirely different challenge.",
    content: `Building a design system is one thing. Making it scale across hundreds of teams and thousands of components is an entirely different challenge. Companies like Google, Airbnb, and Spotify have invested years into their design systems — and the lessons they've learned are invaluable.

## Start with Tokens, Not Components

Design tokens — the atomic values of color, spacing, typography, and motion — are the foundation of any scalable system. Before you build a single component, establish your token vocabulary. This ensures consistency across every surface, from mobile apps to web dashboards.

## The Component Lifecycle

Every component goes through a lifecycle: proposal, design review, implementation, documentation, and deprecation. Formalize this process early. Without governance, design systems become graveyards of outdated components nobody trusts.

## Documentation is the Product

The most beautiful component library is worthless if developers can't figure out how to use it. Invest in interactive documentation, Storybook stories, and usage guidelines. The best design systems treat documentation as a first-class deliverable.

## Versioning and Migration

Semantic versioning isn't just for npm packages. Design system versions communicate breaking changes, deprecations, and new features. Provide migration guides for every major version bump.

Scaling a design system is ultimately a people problem, not a technology problem. Invest in champions, governance structures, and community building.`,
    tags: ["Design Systems", "UI/UX", "Scalability"],
    coverGradient: "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
  },
  {
    id: 3,
    title: "James Webb Space Telescope: Year Three Discoveries",
    slug: "jwst-year-three-discoveries",
    category: "Science",
    author: "Dr. Sarah Kim",
    authorAvatar: "SK",
    date: "2026-04-22",
    readTime: "10 min read",
    excerpt:
      "Three years into its mission, the James Webb Space Telescope continues to shatter our understanding of the early universe, exoplanet atmospheres, and stellar formation.",
    content: `Three years into its mission, the James Webb Space Telescope continues to shatter our understanding of the early universe, exoplanet atmospheres, and stellar formation. The data streaming back from L2 orbit represents the most significant astronomical dataset in history.

## Peering into the First Light

JWST has observed galaxies forming just 200-300 million years after the Big Bang — far earlier than Hubble's reach. These "cosmic dawn" galaxies challenge existing models of galaxy formation. Some are unexpectedly massive, suggesting that star formation was remarkably efficient in the early universe.

## Exoplanet Atmospheres

The telescope's NIRSpec and MIRI instruments have characterized the atmospheres of dozens of exoplanets. Detection of carbon dioxide, methane, and water vapor in multiple planetary systems has refined our understanding of planetary habitability. One super-Earth in the habitable zone of a nearby star showed tentative signs of an oxygen-rich atmosphere.

## Stellar Nurseries in Unprecedented Detail

The Pillars of Creation image, already iconic, has been supplemented by dozens of stellar nursery observations. JWST can peer through the dust that obscures young star-forming regions, revealing protostars in the earliest stages of formation.

## What's Next

The telescope is designed to operate for over 20 years. Mission scientists are now planning deep field surveys that will create the most comprehensive map of the distant universe ever assembled.`,
    tags: ["Space", "Astronomy", "JWST"],
    coverGradient: "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
  },
  {
    id: 4,
    title: "Solo Travel in Southeast Asia: A Complete Guide",
    slug: "solo-travel-southeast-asia",
    category: "Travel",
    author: "Jordan Lee",
    authorAvatar: "JL",
    date: "2026-04-18",
    readTime: "12 min read",
    excerpt:
      "Southeast Asia remains one of the world's great travel destinations — rich culture, incredible food, and an infrastructure built for the modern solo traveler.",
    content: `Southeast Asia remains one of the world's great travel destinations — rich culture, incredible food, and an infrastructure built for the modern solo traveler. Whether you're island-hopping in Thailand or exploring the ancient temples of Cambodia, this region rewards exploration at every turn.

## Planning Your Route

The classic Southeast Asia circuit — Bangkok, Chiang Mai, Luang Prabang, Hanoi, Hoi An, Ho Chi Minh City — takes about 4-6 weeks at a comfortable pace. Budget travelers can do it for $40-60 per day including accommodation, food, and transport.

## Getting Around

Overnight buses and trains are your best friends. The Vietnam train route from Hanoi to Ho Chi Minh City is one of the most scenic rail journeys in Asia. Budget airlines like AirAsia and Vietjet connect major hubs for as little as $20-40.

## Where to Stay

The hostel scene in Southeast Asia is world-class. Party hostels in Bangkok and Pai contrast with serene eco-lodges in northern Laos. Apps like Hostelworld and Booking.com make it easy to compare options.

## Food: Your Greatest Adventure

Street food is not just cheaper — it's better. Vietnam's pho and banh mi, Thailand's pad thai and som tam, Indonesia's nasi goreng — eat where the locals eat. A full meal rarely costs more than $2-3.

## Staying Safe

Solo travel here is generally safe, but standard precautions apply. Keep copies of important documents, use reputable transport, and trust your instincts. Female solo travelers in particular should research destination-specific advice.`,
    tags: ["Travel", "Southeast Asia", "Solo Travel"],
    coverGradient: "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",
  },
  {
    id: 5,
    title: "Mindful Mornings: Building a Routine That Actually Works",
    slug: "mindful-mornings-routine",
    category: "Lifestyle",
    author: "Emma Wilson",
    authorAvatar: "EW",
    date: "2026-04-15",
    readTime: "5 min read",
    excerpt:
      "Morning routines are everywhere — but most of them are productivity theater. Here's how to build one that genuinely improves your wellbeing.",
    content: `Morning routines are everywhere — but most of them are productivity theater. Instagram would have you believe that success requires a 5 AM wake-up, a cold plunge, 45 minutes of meditation, journaling, and a green smoothie before 7 AM. The reality is more nuanced.

## Start with Your Why

Before adding anything to your morning, understand why you want a routine. Is it to reduce stress? Increase focus? Feel more intentional? Your why will determine what belongs in your morning, not someone else's influencer routine.

## The Core Four

Research consistently supports four morning practices: movement (even a 10-minute walk), some form of mindfulness (breathing exercises count), protein-rich breakfast, and protecting the first hour from screens. Beyond these, everything else is optional.

## Building Gradually

Don't overhaul your morning overnight. Add one new habit at a time. Spend two weeks solidifying it before adding another. Habit stacking — attaching new habits to existing anchors — dramatically improves adherence.

## The Night Before

The best morning routines are prepared the evening before. Laying out clothes, prepping breakfast, charging devices, and reviewing tomorrow's schedule reduces morning friction and decision fatigue.

## Grace Over Perfection

Miss a morning? Start fresh tomorrow. A routine that you follow 80% of the time is infinitely more valuable than a perfect routine you abandon after two weeks.`,
    tags: ["Lifestyle", "Wellness", "Productivity"],
    coverGradient: "linear-gradient(135deg, #fa709a 0%, #fee140 100%)",
  },
  {
    id: 6,
    title: "Bootstrapping vs. VC Funding: Making the Right Choice",
    slug: "bootstrapping-vs-vc-funding",
    category: "Business",
    author: "Ryan Torres",
    authorAvatar: "RT",
    date: "2026-04-10",
    readTime: "9 min read",
    excerpt:
      "The startup world glorifies venture capital. But for many founders, bootstrapping leads to better outcomes — and more control over your destiny.",
    content: `The startup world glorifies venture capital. But for many founders, bootstrapping leads to better outcomes — and more control over your destiny. Understanding the tradeoffs is crucial before making the decision.

## The Case for Bootstrapping

Bootstrapped companies grow more slowly but with discipline. Without a runway clock ticking, founders can focus on sustainable unit economics rather than growth at all costs. Companies like Basecamp, Mailchimp, and Notion (early stages) proved that massive businesses can be built without VC.

The biggest advantage: you keep your equity. A bootstrapped $10M ARR business can be more personally valuable than a VC-backed $100M ARR company where the founder owns 5%.

## The Case for VC

Some markets are winner-take-all. Network effects, regulatory moats, and hardware businesses often require large upfront capital that bootstrapping can't provide. VC also brings strategic value: warm intros, operational expertise, and board-level experience.

## The Decision Framework

Ask yourself: Is this a winner-take-all market? Do I need to move faster than organic growth allows? Am I willing to take on investors as partners? Do I have the risk tolerance for the VC treadmill?

If you answered yes to all four, venture capital may be right for you. If you're building a profitable niche business with sustainable growth, bootstrapping is likely the better path.

## The Middle Path

Revenue-based financing, strategic angels, and small seed rounds offer middle-ground options. These provide capital without the pressure of full VC expectations.`,
    tags: ["Business", "Startups", "Funding"],
    coverGradient: "linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%)",
  },
  {
    id: 7,
    title: "WebAssembly in 2026: Beyond the Browser",
    slug: "webassembly-2026-beyond-browser",
    category: "Technology",
    author: "Sam Rivera",
    authorAvatar: "SR",
    date: "2026-04-05",
    readTime: "7 min read",
    excerpt:
      "WebAssembly started as a way to run C++ in browsers. In 2026, it's powering serverless functions, edge computing, and plugin systems across the industry.",
    content: `WebAssembly started as a way to run C++ in browsers. In 2026, it's powering serverless functions, edge computing, and plugin systems across the industry. The WASI (WebAssembly System Interface) standard has matured enough to make Wasm a genuine universal runtime.

## The WASI Revolution

WASI 0.2, finalized in late 2024, introduced component linking and a standard set of system interfaces. This allows Wasm modules to interact with filesystems, networks, and crypto in a sandboxed, portable way. Cloudflare Workers, Fastly Compute, and Fermyon Spin all run on Wasm under the hood.

## Plugin Systems

Extism and similar SDKs have made it trivial to embed Wasm as a plugin runtime. Instead of shipping a Python interpreter or V8 instance, applications now accept Wasm plugins that run in a secure sandbox. This pattern is appearing in everything from API gateways to observability platforms.

## Language Support

Rust and C/C++ remain first-class Wasm targets, but Go, Swift, Kotlin, and Python all have Wasm compilation paths. The Componentize-py project lets Python functions compile to Wasm components — a game-changer for data science plugins.

## The Road Ahead

Garbage collection support (WasmGC) has unlocked Java and Kotlin compilation to Wasm with reasonable performance. Threading and SIMD instructions are now widely supported. The question is no longer whether Wasm is production-ready — it clearly is. The question is how far its reach will extend.`,
    tags: ["WebAssembly", "Technology", "Edge Computing"],
    coverGradient: "linear-gradient(135deg, #30cfd0 0%, #667eea 100%)",
  },
  {
    id: 8,
    title: "Color Theory for Digital Designers",
    slug: "color-theory-digital-designers",
    category: "Design",
    author: "Priya Sharma",
    authorAvatar: "PS",
    date: "2026-03-30",
    readTime: "11 min read",
    excerpt:
      "Understanding color is one of the most powerful skills a designer can develop. This guide covers everything from the basics to advanced color system design.",
    content: `Understanding color is one of the most powerful skills a designer can develop. Beyond aesthetics, color communicates meaning, guides attention, and creates emotional resonance. This guide covers everything from the basics to advanced color system design.

## The Color Wheel Fundamentals

Primary colors (red, yellow, blue in traditional theory; red, green, blue in light) form the basis of all other colors. Complementary colors sit opposite each other on the wheel and create maximum contrast. Analogous colors sit adjacent and create harmony.

## HSL: The Designer's Color Model

Forget RGB. HSL (Hue, Saturation, Lightness) maps directly to how designers think about color. Hue is the color itself, saturation is its intensity, and lightness is its brightness. Manipulating L and S independently gives you complete control over tonal variations.

## Building a Color Palette

Start with a primary brand color. Generate a tonal scale (50 through 950) by varying lightness. Add semantic colors: success (green), warning (amber), error (red). Keep neutral grays slightly warm or cool to complement your primary.

## Accessibility and Contrast

WCAG 2.1 AA requires 4.5:1 contrast for body text and 3:1 for large text. Use tools like Figma's contrast checker or whocanuse.com to verify your palette. Dark mode isn't just about inverting colors — it requires a completely reconsidered palette.

## Emotional Color Psychology

Warm colors (red, orange, yellow) are energizing and attention-grabbing. Cool colors (blue, green, purple) convey trust, calm, and professionalism. Context matters enormously — a red CTA button in a financial app might feel alarming; the same button in a gaming app feels exciting.`,
    tags: ["Design", "Color Theory", "UI/UX"],
    coverGradient: "linear-gradient(135deg, #fd79a8 0%, #6c5ce7 100%)",
  },
  {
    id: 9,
    title: "The Gut-Brain Connection: What Science Now Knows",
    slug: "gut-brain-connection-science",
    category: "Science",
    author: "Dr. Marcus Webb",
    authorAvatar: "MW",
    date: "2026-03-25",
    readTime: "9 min read",
    excerpt:
      "The microbiome's influence on mental health, cognition, and behavior is one of the most exciting frontiers in modern science.",
    content: `The microbiome's influence on mental health, cognition, and behavior is one of the most exciting frontiers in modern science. What researchers are discovering about the gut-brain axis is reshaping psychiatry, neurology, and nutrition.

## The Enteric Nervous System

The gut contains over 500 million neurons — more than the spinal cord. This "second brain" communicates bidirectionally with the central nervous system via the vagus nerve, the enteric nervous system, and the bloodstream. Serotonin, often called the "happiness neurotransmitter," is produced 90% in the gut.

## The Microbiome and Mental Health

Multiple studies now link microbiome composition to depression, anxiety, and even autism spectrum disorders. Germ-free mice show exaggerated stress responses that normalize when specific bacterial strains are introduced. Fecal microbiota transplants (FMT) are being trialed as treatments for treatment-resistant depression.

## Diet as Psychiatry

The SMILES trial (2017) demonstrated that dietary intervention could reduce depression symptoms as effectively as therapy. The Mediterranean diet, rich in fermented foods, fiber, and omega-3s, consistently correlates with better mental health outcomes.

## The Immune Connection

70% of the immune system is gut-associated. Chronic inflammation — driven by poor diet, stress, and sleep deprivation — is increasingly implicated in depression, Alzheimer's, and cardiovascular disease. The microbiome regulates inflammatory responses, creating another pathway between gut health and systemic wellness.

## Practical Implications

Eat diverse whole foods. Include fermented foods (yogurt, kimchi, kefir). Minimize ultra-processed foods. Manage stress. Sleep 7-9 hours. These aren't just diet tips — they're interventions for brain health.`,
    tags: ["Science", "Health", "Microbiome"],
    coverGradient: "linear-gradient(135deg, #0fd850 0%, #f9f047 100%)",
  },
  {
    id: 10,
    title: "Japan Off the Beaten Path: Hidden Gems Beyond Tokyo",
    slug: "japan-off-beaten-path",
    category: "Travel",
    author: "Yuki Tanaka",
    authorAvatar: "YT",
    date: "2026-03-20",
    readTime: "14 min read",
    excerpt:
      "Japan's rural heartland — its mountain villages, ancient pilgrimage trails, and remote onsen — offers a profoundly different experience from its famous cities.",
    content: `Japan's rural heartland — its mountain villages, ancient pilgrimage trails, and remote onsen — offers a profoundly different experience from its famous cities. While Tokyo and Kyoto deserve their fame, the real magic of Japan often lies further afield.

## The Nakasendo Trail

The Nakasendo was one of five major roads in Edo-period Japan, connecting Edo (Tokyo) to Kyoto through the mountains of Honshu. The 500km route took about two weeks to walk in historical times. Today, the best-preserved section between Magome and Tsumago is easily walked in a day — cypress forests, traditional inns, and almost no cars.

## Shikoku's 88 Temple Pilgrimage

The Henro pilgrimage around Shikoku island is 1,200km of trail connecting 88 temples associated with the monk Kukai. Completing it takes 30-60 days on foot. Modern pilgrims travel by bus or car. The trail passes through fishing villages, mountain passes, and sacred hot springs. Foreign pilgrims are warmly welcomed.

## The Tōhoku Region

Devastated by the 2011 earthquake and tsunami, Tōhoku has rebuilt remarkably. The Sanriku Reconstruction National Park coastline — dramatic cliffs, hidden coves, and fishing villages — sees a fraction of the tourists of other Japanese destinations. The Showa Sanriku Railway, restored after the disaster, is one of Japan's most scenic rail lines.

## Staying in a Ryokan

A traditional ryokan experience — futon bedding, multi-course kaiseki dinner, communal onsen — is available outside tourist centers for a fraction of the Kyoto price. Yamanouchi in Nagano and Kurokawa in Kyushu are both excellent bases.

## Practical Notes

JR Pass covers Shinkansen travel. Rural areas often require separate regional passes or cash purchases. Google Maps works excellently even in remote areas. English signage decreases dramatically outside major cities, but Japanese people are unfailingly helpful.`,
    tags: ["Japan", "Travel", "Culture"],
    coverGradient: "linear-gradient(135deg, #f7971e 0%, #ffd200 100%)",
  },
  {
    id: 11,
    title: "Remote Work in 2026: What Actually Works",
    slug: "remote-work-2026",
    category: "Lifestyle",
    author: "Carlos Mendez",
    authorAvatar: "CM",
    date: "2026-03-15",
    readTime: "7 min read",
    excerpt:
      "Six years after the remote work revolution, the dust has settled. Here's what the research and lived experience actually tell us about distributed work.",
    content: `Six years after the remote work revolution, the dust has settled. Here's what the research and lived experience actually tell us about distributed work. The pendulum has swung from "remote for everyone" to "return to office mandates" — the truth, as always, is more nuanced.

## What Remote Work Does Well

Focused, individual work — coding, writing, analysis, design — is often better done remotely. Without office interruptions, people report getting more "deep work" done in fewer hours. Commute time eliminated means more time for family, health, and recovery.

## Where In-Person Wins

Creative brainstorming, relationship building, onboarding, and complex negotiations benefit from physical presence. The serendipitous hallway conversation is real. New employees who've never met their colleagues face genuine career disadvantages in fully remote environments.

## The Hybrid Reality

The most effective model, supported by most recent research, is structured hybrid: 2-3 days remote, 2-3 days in person, with intentionality about what happens when. Teams that synchronize their in-person days see dramatically better outcomes than those using ad-hoc hybrid arrangements.

## Async-First Culture

The biggest failure in remote work isn't the model — it's replicating office communication patterns asynchronously. Replacing in-person meetings with video calls doesn't capture the benefits of remote work. Async-first teams, with strong written culture and clear documentation, consistently outperform their sync-heavy counterparts.

## The Home Environment

Investment in home office setup — monitor, ergonomic chair, good lighting, quality microphone — pays back dramatically. The person who looks and sounds professional on calls is perceived as more competent, regardless of their location.`,
    tags: ["Remote Work", "Lifestyle", "Productivity"],
    coverGradient: "linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%)",
  },
  {
    id: 12,
    title: "The SaaS Pricing Playbook",
    slug: "saas-pricing-playbook",
    category: "Business",
    author: "Nina Okafor",
    authorAvatar: "NO",
    date: "2026-03-08",
    readTime: "10 min read",
    excerpt:
      "Pricing is the highest-leverage decision in your business. Getting it wrong costs you money every single day. Here's how to get it right.",
    content: `Pricing is the highest-leverage decision in your business. Getting it wrong costs you money every single day — either by leaving revenue on the table or by pricing out customers who would have been profitable. Here's how to get it right.

## Value-Based Pricing: The Foundation

Never price based on your costs. Price based on the value you deliver to customers. A tool that saves a senior engineer 5 hours per week is worth far more than the cost of the API calls it makes. Quantify the value: time saved, revenue generated, errors prevented, headcount avoided.

## The Three-Tier Playbook

Good-better-best pricing works because it lets customers self-select into the tier that fits their willingness to pay. The middle tier — your "better" — should be the obvious choice. Price it at 3-5x the basic tier and include most popular features. The premium tier exists partly to make the middle tier feel reasonable.

## Per-Seat vs. Usage-Based

Per-seat pricing is predictable and easy to budget for buyers. Usage-based pricing aligns costs with value but creates revenue volatility. Modern SaaS often combines both: a minimum seat commitment with usage-based overage. This captures predictability for both parties.

## Pricing Page Psychology

Highlight your recommended plan. Show annual pricing by default (it hides the monthly cost). List what's NOT included in lower tiers rather than only what IS included in higher ones. Testimonials on the pricing page reduce hesitation.

## When to Raise Prices

If your churn is low and your NPS is high, you're probably undercharging. Run a pricing experiment on new customers before changing prices for existing ones. Give existing customers advance notice and a lock-in period at current rates.`,
    tags: ["Business", "SaaS", "Pricing"],
    coverGradient: "linear-gradient(135deg, #e96c6c 0%, #ff9a44 100%)",
  },
];

export const POSTS_PER_PAGE = 6;
