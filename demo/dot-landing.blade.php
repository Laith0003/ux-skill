{{-- filename: resources/views/landing/home.blade.php --}}
<!DOCTYPE html>
<html lang="en" dir="ltr" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dot — The internet of what people actually do</title>
    <meta name="description" content="MENA-first loyalty. Show your phone. Earn. Spend. Used by Bashiti, Café Younes, Wild Jordan Center.">

    @vite(['resources/css/app.css', 'resources/js/app.js'])

    <style>
        :root {
            --brand-dot: #0EA5E9;
            --ink: #0A0A0B;
            --canvas: #FFFFFF;
            --hairline: rgba(10, 10, 11, 0.08);
            --whisper: rgba(10, 10, 11, 0.55);
        }

        html, body {
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Geist", system-ui, sans-serif;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            font-feature-settings: "ss01", "cv11";
            letter-spacing: -0.011em;
            background: var(--canvas);
            color: var(--ink);
        }

        [dir="rtl"] body {
            font-family: "SF Arabic", "IBM Plex Sans Arabic", -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
        }

        .display {
            font-weight: 600;
            letter-spacing: -0.034em;
            line-height: 1.02;
        }

        .num-tabular {
            font-variant-numeric: tabular-nums;
            font-feature-settings: "tnum";
        }

        /* Spotlight border card */
        .spotlight-card {
            position: relative;
            background: var(--canvas);
            border: 1px solid var(--hairline);
            border-radius: 18px;
            overflow: hidden;
            isolation: isolate;
            transition: transform 380ms cubic-bezier(0.2, 0.8, 0.2, 1);
        }
        .spotlight-card::before {
            content: "";
            position: absolute;
            inset: -1px;
            border-radius: 19px;
            padding: 1px;
            background: radial-gradient(
                380px circle at var(--mx, -200px) var(--my, -200px),
                rgba(10, 10, 11, 0.42),
                transparent 60%
            );
            -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
            -webkit-mask-composite: xor;
                    mask-composite: exclude;
            opacity: 0;
            transition: opacity 280ms ease;
            pointer-events: none;
            z-index: 1;
        }
        .spotlight-card:hover::before { opacity: 1; }
        .spotlight-card:hover { transform: translateY(-2px); }

        /* Scroll progress path */
        .scroll-path-stroke {
            stroke-dasharray: var(--len, 2400);
            stroke-dashoffset: var(--len, 2400);
            transition: stroke-dashoffset 120ms linear;
        }

        /* Skeleton shimmer */
        @keyframes shimmer {
            0%   { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
        [dir="rtl"] @keyframes shimmer {
            0%   { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }
        .skeleton {
            position: relative;
            background: rgba(10, 10, 11, 0.04);
            border-radius: 8px;
            overflow: hidden;
        }
        .skeleton::after {
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(
                90deg,
                transparent,
                rgba(10, 10, 11, 0.06),
                transparent
            );
            animation: shimmer 1.6s infinite;
        }

        /* Hero stylistic fade */
        .hero-fade {
            background: radial-gradient(
                circle at 70% 40%,
                rgba(10, 10, 11, 0.03),
                transparent 55%
            );
        }
        [dir="rtl"] .hero-fade {
            background: radial-gradient(
                circle at 30% 40%,
                rgba(10, 10, 11, 0.03),
                transparent 55%
            );
        }

        /* Brand dot */
        .brand-dot {
            display: inline-block;
            width: 0.5em;
            height: 0.5em;
            border-radius: 999px;
            background: var(--brand-dot);
            vertical-align: 0.08em;
        }

        /* Asset card — receipt mock */
        .receipt {
            background: var(--canvas);
            border: 1px solid var(--hairline);
            border-radius: 22px;
            box-shadow:
                0 1px 0 rgba(10, 10, 11, 0.04),
                0 24px 60px -28px rgba(10, 10, 11, 0.18);
        }

        /* Subtle motion on entry */
        @keyframes rise-in {
            from { opacity: 0; transform: translateY(8px); }
            to   { opacity: 1; transform: translateY(0); }
        }
        .rise-in { animation: rise-in 700ms cubic-bezier(0.2, 0.8, 0.2, 1) both; }

        /* Logo wall — grayscale tasteful */
        .brand-wordmark {
            font-weight: 500;
            letter-spacing: -0.018em;
            color: rgba(10, 10, 11, 0.62);
            transition: color 220ms ease;
        }
        .brand-wordmark:hover { color: var(--ink); }

        @media (prefers-reduced-motion: reduce) {
            .rise-in, .skeleton::after { animation: none; }
            .spotlight-card, .spotlight-card:hover { transition: none; transform: none; }
        }
    </style>
</head>

<body
    class="antialiased bg-white text-zinc-950 selection:bg-zinc-950 selection:text-white"
    x-data="dotLanding()"
    x-init="init()"
>

    {{-- ──────────────────────────────────────────
         Scroll progress path (subtle SVG line)
         ────────────────────────────────────────── --}}
    <div
        class="pointer-events-none fixed inset-y-0 start-6 z-40 hidden md:block"
        aria-hidden="true"
    >
        <svg
            class="h-full w-6"
            viewBox="0 0 24 1000"
            preserveAspectRatio="none"
            fill="none"
        >
            {{-- Path itself: subtle hairline guide --}}
            <path
                d="M 12 0 C 12 180, 4 220, 4 380 S 20 540, 20 680 S 12 820, 12 1000"
                stroke="rgba(10,10,11,0.06)"
                stroke-width="1"
            />
            {{-- Animated drawn path on scroll --}}
            <path
                d="M 12 0 C 12 180, 4 220, 4 380 S 20 540, 20 680 S 12 820, 12 1000"
                stroke="var(--ink)"
                stroke-width="1.5"
                stroke-linecap="round"
                class="scroll-path-stroke"
                :style="`--len: 2400; stroke-dashoffset: ${2400 - (scrollProgress * 2400)};`"
            />
            {{-- Brand-dot puck riding the line --}}
            <circle
                r="3.5"
                fill="var(--brand-dot)"
                :cx="pathPoint.x"
                :cy="pathPoint.y"
                style="transition: cx 120ms linear, cy 120ms linear;"
            />
        </svg>
    </div>

    {{-- ──────────────────────────────────────────
         Top nav
         ────────────────────────────────────────── --}}
    <header class="relative z-30">
        <div class="mx-auto max-w-7xl px-6 lg:px-10 pt-7 flex items-center justify-between">
            <a href="/" class="inline-flex items-center gap-2.5" aria-label="Dot home">
                <span class="brand-dot" style="width: 12px; height: 12px;"></span>
                <span class="text-[15px] font-medium tracking-tight">Dot</span>
            </a>

            <nav class="hidden md:flex items-center gap-9 text-[14px] text-zinc-700">
                <a href="#how" class="hover:text-zinc-950 transition">How it works</a>
                <a href="#partners" class="hover:text-zinc-950 transition">For partners</a>
                <a href="#proof" class="hover:text-zinc-950 transition">Who's on Dot</a>
            </nav>

            <a
                href="#join"
                class="inline-flex items-center gap-2 rounded-full bg-zinc-950 text-white text-[13px] font-medium px-4 py-2 hover:bg-zinc-800 transition"
            >
                Join Dot
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="rtl:rotate-180">
                    <path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>
                </svg>
            </a>
        </div>
    </header>

    {{-- ──────────────────────────────────────────
         1. HERO — asymmetric split
            Text starts (logical-start), asset ends.
            NEVER centered. Subtle radial fade in the asset side.
         ────────────────────────────────────────── --}}
    <section class="relative hero-fade">
        <div class="mx-auto max-w-7xl px-6 lg:px-10 pt-20 lg:pt-28 pb-24 lg:pb-32">
            <div class="grid grid-cols-12 gap-y-14 lg:gap-x-12 items-end">

                {{-- Text — logical start side, 7 cols --}}
                <div class="col-span-12 lg:col-span-7 lg:ps-2">
                    <div class="inline-flex items-center gap-2 rounded-full border border-zinc-200 bg-white/70 backdrop-blur px-3 py-1 text-[12px] text-zinc-600 mb-7 rise-in">
                        <span class="brand-dot" style="width: 6px; height: 6px;"></span>
                        <span>Live in Amman. Bashiti, Café Younes, Wild Jordan Center.</span>
                    </div>

                    <h1 class="display text-[44px] sm:text-[60px] lg:text-[76px] xl:text-[86px] text-zinc-950 rise-in" style="animation-delay: 60ms;">
                        Beyond likes. <br class="hidden sm:block">
                        Beyond clicks.<span class="brand-dot align-baseline" style="width: 0.16em; height: 0.16em; margin-inline-start: 0.06em;"></span>
                    </h1>

                    <p class="mt-7 max-w-[34rem] text-[18px] lg:text-[19px] leading-[1.55] text-zinc-600 rise-in" style="animation-delay: 140ms;">
                        Dot is the internet of what people actually do. One wallet for every shop you walk into — show your phone, earn, spend. No cards, no apps to download for each brand.
                    </p>

                    <div class="mt-10 flex flex-col sm:flex-row items-start sm:items-center gap-4 rise-in" style="animation-delay: 220ms;">
                        <a
                            href="#join"
                            class="inline-flex items-center gap-2 rounded-full bg-zinc-950 text-white text-[15px] font-medium px-5 py-3 hover:bg-zinc-800 transition"
                        >
                            Get the wallet
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="rtl:rotate-180">
                                <path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>
                            </svg>
                        </a>

                        <a
                            href="#how"
                            class="inline-flex items-center gap-2 text-[15px] text-zinc-700 hover:text-zinc-950 transition"
                        >
                            See how it works
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M12 5v14"/><path d="m19 12-7 7-7-7"/>
                            </svg>
                        </a>
                    </div>

                    {{-- Live counter, organic number --}}
                    <div class="mt-14 flex items-center gap-6 text-[13px] text-zinc-500 rise-in" style="animation-delay: 320ms;">
                        <div class="flex items-center gap-2">
                            <span class="relative flex h-2 w-2">
                                <span class="absolute inline-flex h-full w-full rounded-full bg-emerald-500 opacity-60 animate-ping"></span>
                                <span class="relative inline-flex h-2 w-2 rounded-full bg-emerald-500"></span>
                            </span>
                            <span class="num-tabular">23,847</span>
                            <span>members in Amman</span>
                        </div>
                        <div class="hidden sm:block h-3 w-px bg-zinc-200"></div>
                        <div class="hidden sm:block">
                            <span class="num-tabular">47.2%</span> return within 30 days
                        </div>
                    </div>
                </div>

                {{-- Asset side — receipt mock + scan ticket. Offset down, asymmetric. --}}
                <div class="col-span-12 lg:col-span-5 lg:translate-y-8 rise-in" style="animation-delay: 180ms;">
                    <div class="relative">

                        {{-- Background plate --}}
                        <div class="absolute -inset-x-6 -inset-y-8 lg:-inset-x-10 lg:-inset-y-12 bg-zinc-100/60 rounded-[28px]" aria-hidden="true"></div>

                        {{-- Receipt — earn event --}}
                        <div class="receipt relative p-7 sm:p-8 max-w-[420px] ms-auto">

                            <div class="flex items-center justify-between">
                                <div class="flex items-center gap-2">
                                    <span class="brand-dot" style="width: 9px; height: 9px;"></span>
                                    <span class="text-[13px] font-medium text-zinc-700">Dot</span>
                                </div>
                                <span class="text-[12px] text-zinc-400 num-tabular">14:32</span>
                            </div>

                            <div class="mt-6 flex items-baseline gap-2">
                                <span class="display text-[54px] num-tabular">+50</span>
                                <span class="text-[15px] text-zinc-500">points</span>
                            </div>

                            <p class="mt-1 text-[14px] text-zinc-500">
                                Bashiti Hardware, Mecca Street
                            </p>

                            <div class="mt-7 h-px bg-zinc-100"></div>

                            <dl class="mt-6 space-y-3 text-[13px]">
                                <div class="flex items-center justify-between">
                                    <dt class="text-zinc-500">Spent</dt>
                                    <dd class="num-tabular text-zinc-800">23.50 JOD</dd>
                                </div>
                                <div class="flex items-center justify-between">
                                    <dt class="text-zinc-500">Tier</dt>
                                    <dd class="inline-flex items-center gap-1.5">
                                        <span class="inline-block w-1.5 h-1.5 rounded-full bg-zinc-950"></span>
                                        <span class="text-zinc-800">Silver</span>
                                    </dd>
                                </div>
                                <div class="flex items-center justify-between">
                                    <dt class="text-zinc-500">Balance</dt>
                                    <dd class="num-tabular text-zinc-800">1,260 pts</dd>
                                </div>
                            </dl>

                            <div class="mt-8 grid grid-cols-3 gap-2">
                                <button class="col-span-2 inline-flex items-center justify-center gap-2 rounded-xl bg-zinc-950 text-white text-[13px] py-3 hover:bg-zinc-800 transition">
                                    Redeem
                                </button>
                                <button class="inline-flex items-center justify-center rounded-xl border border-zinc-200 text-[13px] text-zinc-700 py-3 hover:bg-zinc-50 transition">
                                    Send
                                </button>
                            </div>
                        </div>

                        {{-- Floating stamp card chip — secondary asset --}}
                        <div class="absolute -bottom-6 -start-4 sm:-start-8 lg:-start-12 receipt p-4 sm:p-5 w-[220px] sm:w-[240px] rotate-[-3deg]">
                            <p class="text-[11px] uppercase tracking-[0.14em] text-zinc-400">Stamp card</p>
                            <p class="mt-1 text-[13px] text-zinc-700">Café Younes — 8 cups</p>

                            <div class="mt-3 grid grid-cols-8 gap-1.5" aria-hidden="true">
                                @for ($i = 0; $i < 8; $i++)
                                    @if ($i < 6)
                                        <span class="aspect-square rounded-full bg-zinc-950"></span>
                                    @else
                                        <span class="aspect-square rounded-full border border-dashed border-zinc-300"></span>
                                    @endif
                                @endfor
                            </div>

                            <p class="mt-3 text-[12px] text-zinc-500 num-tabular">2 more for a free flat white</p>
                        </div>

                    </div>
                </div>
            </div>
        </div>
    </section>

    {{-- ──────────────────────────────────────────
         2. VALUE PROPS — zig-zag, NOT 3 equal cards.
            Three rows of asymmetric layouts.
            Each block is a spotlight-border card.
         ────────────────────────────────────────── --}}
    <section class="relative py-24 lg:py-36">
        <div class="mx-auto max-w-7xl px-6 lg:px-10">

            <div class="grid grid-cols-12 mb-20 lg:mb-28">
                <div class="col-span-12 lg:col-span-7 lg:col-start-2">
                    <p class="text-[12px] uppercase tracking-[0.18em] text-zinc-500 mb-5">Why Dot</p>
                    <h2 class="display text-[36px] sm:text-[48px] lg:text-[58px] text-zinc-950">
                        Loyalty without the loyalty card.
                    </h2>
                </div>
            </div>

            {{-- Row 1: large card on start, narrow column on end --}}
            <div class="grid grid-cols-12 gap-6 lg:gap-8">
                <article
                    class="spotlight-card col-span-12 lg:col-span-8 p-8 lg:p-12"
                    @mousemove="setSpotlight($event)"
                    @mouseleave="clearSpotlight($event)"
                >
                    <div class="flex items-start gap-5">
                        <div class="shrink-0 mt-1">
                            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" class="text-zinc-950">
                                <rect x="3" y="5" width="18" height="14" rx="3"/>
                                <path d="M3 10h18"/>
                                <path d="M7 15h.01"/>
                                <path d="M11 15h2"/>
                            </svg>
                        </div>
                        <div class="flex-1">
                            <h3 class="text-[22px] lg:text-[26px] font-semibold tracking-tight text-zinc-950">
                                Your phone is your wallet.
                            </h3>
                            <p class="mt-3 text-[16px] lg:text-[17px] leading-[1.55] text-zinc-600 max-w-[40rem]">
                                Tell the cashier your number. They tap it in. Points landed before your card swipe finishes. No app open. No QR. No staff training beyond a single screen.
                            </p>

                            <div class="mt-8 inline-flex items-center gap-3 rounded-2xl border border-zinc-200 bg-zinc-50/50 px-4 py-3">
                                <span class="text-[12px] text-zinc-500">Phone</span>
                                <span class="font-medium text-zinc-950 num-tabular tracking-wide">+962 79 786 8335</span>
                                <span class="h-3 w-px bg-zinc-200"></span>
                                <span class="inline-flex items-center gap-1.5 text-[12px] text-emerald-700">
                                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>
                                    Matched
                                </span>
                            </div>
                        </div>
                    </div>
                </article>

                {{-- Narrow card — quote --}}
                <article
                    class="spotlight-card col-span-12 lg:col-span-4 p-8 lg:p-10 flex flex-col"
                    @mousemove="setSpotlight($event)"
                    @mouseleave="clearSpotlight($event)"
                >
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="text-zinc-300">
                        <path d="M3 21c3 0 7-1 7-8V5c0-1.25-.756-2.017-2-2H4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2 1 0 1 0 1 1v1c0 1-1 2-2 2s-1 .008-1 1.031V20c0 1 0 1 1 1z"/>
                        <path d="M15 21c3 0 7-1 7-8V5c0-1.25-.757-2.017-2-2h-4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2h.75c0 2.25.25 4-2.75 4v3c0 1 0 1 1 1z"/>
                    </svg>
                    <p class="mt-5 text-[17px] leading-[1.55] text-zinc-800">
                        I stopped carrying three stamp cards. My customers don't even need to remember they're members. They just walk in.
                    </p>
                    <div class="mt-auto pt-8 flex items-center gap-3">
                        <span class="inline-flex items-center justify-center w-9 h-9 rounded-full bg-zinc-950 text-white text-[13px] font-medium">LT</span>
                        <div>
                            <p class="text-[14px] font-medium text-zinc-950">Lina Touma</p>
                            <p class="text-[12px] text-zinc-500">Owner, Café Younes Jabal Amman</p>
                        </div>
                    </div>
                </article>
            </div>

            {{-- Row 2: zig — narrow start, large end --}}
            <div class="grid grid-cols-12 gap-6 lg:gap-8 mt-6 lg:mt-8">
                {{-- Stat block --}}
                <article
                    class="spotlight-card col-span-12 lg:col-span-5 p-8 lg:p-10"
                    @mousemove="setSpotlight($event)"
                    @mouseleave="clearSpotlight($event)"
                >
                    <p class="text-[12px] uppercase tracking-[0.16em] text-zinc-500">Hidden Profile</p>
                    <p class="mt-5 display text-[44px] lg:text-[52px] num-tabular">1.7×</p>
                    <p class="mt-2 text-[15px] text-zinc-600 max-w-[20rem]">
                        Average spend uplift in the first 90 days after a customer's profile connects across two or more brands.
                    </p>
                    <div class="mt-7 h-px bg-zinc-100"></div>
                    <p class="mt-5 text-[12px] text-zinc-500">
                        Measured across 14 Bashiti branches, Q1 2026.
                    </p>
                </article>

                {{-- Large card — cross-merchant graph --}}
                <article
                    class="spotlight-card col-span-12 lg:col-span-7 p-8 lg:p-12"
                    @mousemove="setSpotlight($event)"
                    @mouseleave="clearSpotlight($event)"
                >
                    <div class="flex items-start gap-5">
                        <div class="shrink-0 mt-1">
                            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" class="text-zinc-950">
                                <circle cx="12" cy="12" r="3"/>
                                <circle cx="5" cy="5" r="2"/>
                                <circle cx="19" cy="5" r="2"/>
                                <circle cx="5" cy="19" r="2"/>
                                <circle cx="19" cy="19" r="2"/>
                                <path d="m7 7 3 3"/><path d="m14 14 3 3"/><path d="m17 7-3 3"/><path d="m7 17 3-3"/>
                            </svg>
                        </div>
                        <div class="flex-1">
                            <h3 class="text-[22px] lg:text-[26px] font-semibold tracking-tight text-zinc-950">
                                One profile, every shop you visit.
                            </h3>
                            <p class="mt-3 text-[16px] lg:text-[17px] leading-[1.55] text-zinc-600 max-w-[40rem]">
                                Sign in once. Dot quietly surfaces every loyalty status you already earned across the network — the stamps, the unspent points, the silver tier you didn't know you had. The first time you open Dot, you don't start from zero.
                            </p>

                            {{-- Mini graph mock — three brand nodes connected to a phone node --}}
                            <div class="mt-8 grid grid-cols-12 gap-3 items-center">
                                <div class="col-span-3 flex flex-col items-center gap-2">
                                    <span class="inline-flex w-12 h-12 rounded-2xl items-center justify-center bg-zinc-50 border border-zinc-200 text-[11px] font-medium text-zinc-700">BH</span>
                                    <span class="text-[11px] text-zinc-500">Bashiti</span>
                                </div>
                                <div class="col-span-3 flex flex-col items-center gap-2">
                                    <span class="inline-flex w-12 h-12 rounded-2xl items-center justify-center bg-zinc-50 border border-zinc-200 text-[11px] font-medium text-zinc-700">CY</span>
                                    <span class="text-[11px] text-zinc-500">Café Younes</span>
                                </div>
                                <div class="col-span-3 flex flex-col items-center gap-2">
                                    <span class="inline-flex w-12 h-12 rounded-2xl items-center justify-center bg-zinc-50 border border-zinc-200 text-[11px] font-medium text-zinc-700">ML</span>
                                    <span class="text-[11px] text-zinc-500">Mlabbas</span>
                                </div>
                                <div class="col-span-3 flex flex-col items-center gap-2">
                                    <span class="inline-flex w-12 h-12 rounded-2xl items-center justify-center bg-zinc-950 text-white text-[11px] font-medium">
                                        <span class="brand-dot" style="background: #fff; width: 9px; height: 9px;"></span>
                                    </span>
                                    <span class="text-[11px] text-zinc-700 font-medium">You</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </article>
            </div>

            {{-- Row 3: full-width wide card --}}
            <div class="grid grid-cols-12 gap-6 lg:gap-8 mt-6 lg:mt-8">
                <article
                    class="spotlight-card col-span-12 p-8 lg:p-12"
                    @mousemove="setSpotlight($event)"
                    @mouseleave="clearSpotlight($event)"
                >
                    <div class="grid grid-cols-12 gap-y-8 lg:gap-x-12 items-center">
                        <div class="col-span-12 lg:col-span-7">
                            <div class="flex items-start gap-5">
                                <div class="shrink-0 mt-1">
                                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" class="text-zinc-950">
                                        <path d="M12 2v4"/>
                                        <path d="M12 18v4"/>
                                        <path d="m4.93 4.93 2.83 2.83"/>
                                        <path d="m16.24 16.24 2.83 2.83"/>
                                        <path d="M2 12h4"/>
                                        <path d="M18 12h4"/>
                                        <path d="m4.93 19.07 2.83-2.83"/>
                                        <path d="m16.24 7.76 2.83-2.83"/>
                                    </svg>
                                </div>
                                <div>
                                    <h3 class="text-[22px] lg:text-[26px] font-semibold tracking-tight text-zinc-950">
                                        Earned status stays earned.
                                    </h3>
                                    <p class="mt-3 text-[16px] lg:text-[17px] leading-[1.55] text-zinc-600 max-w-[36rem]">
                                        A refund won't drop you back to bronze. Once you cross a tier, you stay above the line — Dot tracks lifetime, not just the last 30 days.
                                    </p>
                                </div>
                            </div>
                        </div>

                        {{-- Tier ladder visual --}}
                        <div class="col-span-12 lg:col-span-5">
                            <div class="rounded-2xl border border-zinc-200 bg-zinc-50/50 p-5">
                                <div class="space-y-3">
                                    <div class="flex items-center justify-between text-[13px]">
                                        <div class="flex items-center gap-2.5">
                                            <span class="inline-block w-2 h-2 rounded-full bg-zinc-300"></span>
                                            <span class="text-zinc-600">Bronze</span>
                                        </div>
                                        <span class="text-zinc-400 num-tabular">0 – 499</span>
                                    </div>
                                    <div class="flex items-center justify-between text-[13px]">
                                        <div class="flex items-center gap-2.5">
                                            <span class="inline-block w-2 h-2 rounded-full bg-zinc-950"></span>
                                            <span class="text-zinc-950 font-medium">Silver</span>
                                        </div>
                                        <span class="text-zinc-600 num-tabular">500 – 1,999</span>
                                    </div>
                                    <div class="flex items-center justify-between text-[13px]">
                                        <div class="flex items-center gap-2.5">
                                            <span class="inline-block w-2 h-2 rounded-full bg-zinc-300"></span>
                                            <span class="text-zinc-600">Gold</span>
                                        </div>
                                        <span class="text-zinc-400 num-tabular">2,000+</span>
                                    </div>
                                </div>
                                <div class="mt-5 h-1.5 rounded-full bg-zinc-200 overflow-hidden">
                                    <div class="h-full bg-zinc-950" style="width: 63%;"></div>
                                </div>
                                <p class="mt-3 text-[12px] text-zinc-500 num-tabular">
                                    1,260 / 2,000 to Gold
                                </p>
                            </div>
                        </div>
                    </div>
                </article>
            </div>

        </div>
    </section>

    {{-- ──────────────────────────────────────────
         3. SOCIAL PROOF — clean logo wall
            Five real Jordanian brands as styled wordmarks.
         ────────────────────────────────────────── --}}
    <section id="proof" class="relative border-y border-zinc-100 py-20 lg:py-24 bg-zinc-50/30">
        <div class="mx-auto max-w-7xl px-6 lg:px-10">

            <div class="grid grid-cols-12 items-end gap-y-8 mb-14 lg:mb-16">
                <div class="col-span-12 lg:col-span-6">
                    <p class="text-[12px] uppercase tracking-[0.18em] text-zinc-500 mb-4">On Dot today</p>
                    <h2 class="display text-[32px] sm:text-[40px] lg:text-[44px] text-zinc-950">
                        Five Jordanian originals.<br>
                        One wallet.
                    </h2>
                </div>
                <div class="col-span-12 lg:col-span-5 lg:col-start-8 lg:text-end">
                    <p class="text-[15px] text-zinc-600 max-w-[30rem] lg:ms-auto">
                        From Mecca Street tools to Wadi Rum gift shops. Pilot live since February 2026.
                    </p>
                </div>
            </div>

            {{-- Asymmetric brand strip — 5 items with deliberate uneven widths --}}
            <div class="grid grid-cols-12 gap-y-10 lg:gap-x-10 items-center">
                <div class="col-span-6 sm:col-span-4 lg:col-span-3">
                    <p class="brand-wordmark text-[22px] lg:text-[26px]">Bashiti<span class="text-zinc-400 font-normal"> Hardware</span></p>
                </div>
                <div class="col-span-6 sm:col-span-4 lg:col-span-2">
                    <p class="brand-wordmark text-[20px] lg:text-[22px] italic">Café Younes</p>
                </div>
                <div class="col-span-12 sm:col-span-4 lg:col-span-3 lg:text-center">
                    <p class="brand-wordmark text-[18px] lg:text-[20px] tracking-[0.04em] uppercase">Wild Jordan</p>
                </div>
                <div class="col-span-6 sm:col-span-6 lg:col-span-2">
                    <p class="brand-wordmark text-[22px] lg:text-[24px] font-semibold">Mlabbas.</p>
                </div>
                <div class="col-span-6 sm:col-span-6 lg:col-span-2 lg:text-end">
                    <p class="brand-wordmark text-[18px] lg:text-[19px]">Casper &amp; Gambini's</p>
                </div>
            </div>

            {{-- Lower row — receipts shimmer (skeleton showing "live partner feed loading") --}}
            <div class="mt-16 lg:mt-20 grid grid-cols-12 gap-6 lg:gap-8" x-data="{ ready: false }" x-init="setTimeout(() => ready = true, 1400)">

                {{-- Live event ticker — real once "ready" --}}
                <div class="col-span-12 lg:col-span-7">
                    <p class="text-[12px] uppercase tracking-[0.16em] text-zinc-500 mb-5">Live event feed</p>

                    <ul class="space-y-3" role="list">
                        {{-- Event 1 --}}
                        <li class="flex items-center justify-between rounded-xl border border-zinc-100 bg-white p-4">
                            <template x-if="!ready">
                                <div class="flex items-center gap-3 w-full">
                                    <div class="skeleton w-9 h-9 rounded-full"></div>
                                    <div class="flex-1 space-y-2">
                                        <div class="skeleton h-3 w-44"></div>
                                        <div class="skeleton h-2.5 w-28"></div>
                                    </div>
                                    <div class="skeleton h-4 w-14"></div>
                                </div>
                            </template>
                            <template x-if="ready">
                                <div class="flex items-center justify-between w-full rise-in">
                                    <div class="flex items-center gap-3">
                                        <span class="inline-flex items-center justify-center w-9 h-9 rounded-full bg-zinc-950 text-white text-[12px] font-medium">BK</span>
                                        <div>
                                            <p class="text-[14px] text-zinc-950"><span class="font-medium">Bashar Kuzbari</span> earned 50 pts</p>
                                            <p class="text-[12px] text-zinc-500">Bashiti Hardware — 14 sec ago</p>
                                        </div>
                                    </div>
                                    <span class="text-[13px] num-tabular text-emerald-700">+50</span>
                                </div>
                            </template>
                        </li>
                        {{-- Event 2 --}}
                        <li class="flex items-center justify-between rounded-xl border border-zinc-100 bg-white p-4">
                            <template x-if="!ready">
                                <div class="flex items-center gap-3 w-full">
                                    <div class="skeleton w-9 h-9 rounded-full"></div>
                                    <div class="flex-1 space-y-2">
                                        <div class="skeleton h-3 w-52"></div>
                                        <div class="skeleton h-2.5 w-24"></div>
                                    </div>
                                    <div class="skeleton h-4 w-16"></div>
                                </div>
                            </template>
                            <template x-if="ready">
                                <div class="flex items-center justify-between w-full rise-in" style="animation-delay: 60ms;">
                                    <div class="flex items-center gap-3">
                                        <span class="inline-flex items-center justify-center w-9 h-9 rounded-full bg-zinc-950 text-white text-[12px] font-medium">MH</span>
                                        <div>
                                            <p class="text-[14px] text-zinc-950"><span class="font-medium">Mira Halawani</span> redeemed a flat white</p>
                                            <p class="text-[12px] text-zinc-500">Café Younes — 1 min ago</p>
                                        </div>
                                    </div>
                                    <span class="text-[13px] num-tabular text-zinc-500">-180</span>
                                </div>
                            </template>
                        </li>
                        {{-- Event 3 --}}
                        <li class="flex items-center justify-between rounded-xl border border-zinc-100 bg-white p-4">
                            <template x-if="!ready">
                                <div class="flex items-center gap-3 w-full">
                                    <div class="skeleton w-9 h-9 rounded-full"></div>
                                    <div class="flex-1 space-y-2">
                                        <div class="skeleton h-3 w-40"></div>
                                        <div class="skeleton h-2.5 w-32"></div>
                                    </div>
                                    <div class="skeleton h-4 w-14"></div>
                                </div>
                            </template>
                            <template x-if="ready">
                                <div class="flex items-center justify-between w-full rise-in" style="animation-delay: 120ms;">
                                    <div class="flex items-center gap-3">
                                        <span class="inline-flex items-center justify-center w-9 h-9 rounded-full bg-zinc-950 text-white text-[12px] font-medium">AT</span>
                                        <div>
                                            <p class="text-[14px] text-zinc-950"><span class="font-medium">Adnan Tabbaa</span> reached Silver</p>
                                            <p class="text-[12px] text-zinc-500">Wild Jordan Center — 3 min ago</p>
                                        </div>
                                    </div>
                                    <span class="inline-flex items-center gap-1 text-[12px] text-zinc-700">
                                        <span class="w-1.5 h-1.5 rounded-full bg-zinc-950"></span>
                                        Silver
                                    </span>
                                </div>
                            </template>
                        </li>
                    </ul>
                </div>

                {{-- Aggregate, organic numbers --}}
                <div class="col-span-12 lg:col-span-5">
                    <p class="text-[12px] uppercase tracking-[0.16em] text-zinc-500 mb-5">Last 30 days</p>

                    <dl class="space-y-6">
                        <div class="flex items-baseline justify-between border-b border-zinc-100 pb-5">
                            <dt class="text-[14px] text-zinc-600">Points awarded</dt>
                            <dd class="display text-[28px] num-tabular">2,418,560</dd>
                        </div>
                        <div class="flex items-baseline justify-between border-b border-zinc-100 pb-5">
                            <dt class="text-[14px] text-zinc-600">Redemptions</dt>
                            <dd class="display text-[28px] num-tabular">8,734</dd>
                        </div>
                        <div class="flex items-baseline justify-between">
                            <dt class="text-[14px] text-zinc-600">Return rate within 30 days</dt>
                            <dd class="display text-[28px] num-tabular">47.2<span class="text-[18px] text-zinc-400">%</span></dd>
                        </div>
                    </dl>
                </div>
            </div>
        </div>
    </section>

    {{-- ──────────────────────────────────────────
         4. HOW IT WORKS — three numbered steps
         ────────────────────────────────────────── --}}
    <section id="how" class="relative py-24 lg:py-36">
        <div class="mx-auto max-w-7xl px-6 lg:px-10">

            <div class="grid grid-cols-12 mb-16 lg:mb-24">
                <div class="col-span-12 lg:col-span-6">
                    <p class="text-[12px] uppercase tracking-[0.18em] text-zinc-500 mb-4">How it works</p>
                    <h2 class="display text-[36px] sm:text-[44px] lg:text-[54px] text-zinc-950">
                        Show your phone.<br>
                        Earn. Spend.
                    </h2>
                </div>
            </div>

            <ol class="grid grid-cols-12 gap-y-12 lg:gap-x-10" role="list">
                {{-- Step 1 --}}
                <li class="col-span-12 lg:col-span-4">
                    <div class="flex items-baseline gap-4 mb-5">
                        <span class="display text-[44px] num-tabular text-zinc-300">01</span>
                        <span class="h-px flex-1 bg-zinc-200 mt-3"></span>
                    </div>
                    <h3 class="text-[20px] font-semibold tracking-tight text-zinc-950">Walk in. Say your number.</h3>
                    <p class="mt-3 text-[15px] leading-[1.6] text-zinc-600 max-w-[18rem]">
                        First visit, the cashier types your phone. Two seconds. Dot recognizes you the moment your number lands.
                    </p>
                </li>

                {{-- Step 2 — offset slightly down for asymmetry --}}
                <li class="col-span-12 lg:col-span-4 lg:translate-y-10">
                    <div class="flex items-baseline gap-4 mb-5">
                        <span class="display text-[44px] num-tabular text-zinc-300">02</span>
                        <span class="h-px flex-1 bg-zinc-200 mt-3"></span>
                    </div>
                    <h3 class="text-[20px] font-semibold tracking-tight text-zinc-950">Points land before your receipt prints.</h3>
                    <p class="mt-3 text-[15px] leading-[1.6] text-zinc-600 max-w-[18rem]">
                        No QR scan, no app to open. The transaction itself is the trigger. You get an SMS that says "50 points added."
                    </p>
                </li>

                {{-- Step 3 --}}
                <li class="col-span-12 lg:col-span-4">
                    <div class="flex items-baseline gap-4 mb-5">
                        <span class="display text-[44px] num-tabular text-zinc-300">03</span>
                        <span class="h-px flex-1 bg-zinc-200 mt-3"></span>
                    </div>
                    <h3 class="text-[20px] font-semibold tracking-tight text-zinc-950">Spend anywhere on the network.</h3>
                    <p class="mt-3 text-[15px] leading-[1.6] text-zinc-600 max-w-[18rem]">
                        Cup of coffee at Café Younes. Drill bits at Bashiti. Tier perks at Wild Jordan. One wallet, every shop.
                    </p>
                </li>
            </ol>
        </div>
    </section>

    {{-- ──────────────────────────────────────────
         5. FOR PARTNERS — one-line proposition + CTA
         ────────────────────────────────────────── --}}
    <section id="partners" class="relative">
        <div class="mx-auto max-w-7xl px-6 lg:px-10 py-20 lg:py-28 border-t border-zinc-100">
            <div class="grid grid-cols-12 gap-y-10 lg:gap-x-12 items-end">

                <div class="col-span-12 lg:col-span-7">
                    <p class="text-[12px] uppercase tracking-[0.18em] text-zinc-500 mb-5">For partners</p>
                    <h2 class="display text-[32px] sm:text-[40px] lg:text-[48px] text-zinc-950 max-w-[34rem]">
                        Plug Dot into your POS in an afternoon.
                    </h2>
                    <p class="mt-5 text-[16px] lg:text-[17px] text-zinc-600 max-w-[34rem] leading-[1.55]">
                        Direct Odoo and Shopify connectors. Cashier app for everything else. Set your earn rate and rules in a dashboard built for shop owners, not engineers.
                    </p>
                </div>

                <div class="col-span-12 lg:col-span-5 lg:text-end">
                    <a
                        href="/partners"
                        class="inline-flex items-center gap-2 rounded-full border border-zinc-950 text-zinc-950 text-[15px] font-medium px-5 py-3 hover:bg-zinc-950 hover:text-white transition"
                    >
                        See partner pricing
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="rtl:rotate-180">
                            <path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>
                        </svg>
                    </a>
                    <p class="mt-4 text-[12px] text-zinc-500">
                        Or write to partners&#64;thedotwallet.com
                    </p>
                </div>
            </div>
        </div>
    </section>

    {{-- ──────────────────────────────────────────
         6. FINAL CTA — large headline + phone-only join form (HTMX)
         ────────────────────────────────────────── --}}
    <section id="join" class="relative bg-zinc-950 text-white">
        <div class="mx-auto max-w-7xl px-6 lg:px-10 py-24 lg:py-36">
            <div class="grid grid-cols-12 gap-y-12 lg:gap-x-12 items-end">

                <div class="col-span-12 lg:col-span-7">
                    <h2 class="display text-[40px] sm:text-[56px] lg:text-[72px] leading-[1.02]">
                        Join the wallet that<br>
                        already knows you.<span class="brand-dot align-baseline" style="width: 0.14em; height: 0.14em; margin-inline-start: 0.06em;"></span>
                    </h2>
                </div>

                {{-- Phone-only join form --}}
                <div class="col-span-12 lg:col-span-5" x-data="{ submitted: false }">
                    <form
                        hx-post="/join"
                        hx-target="#join-result"
                        hx-swap="innerHTML"
                        @htmx:after-request="submitted = true"
                        class="space-y-4"
                        novalidate
                    >
                        <label for="phone" class="block text-[12px] uppercase tracking-[0.16em] text-zinc-500">
                            Your phone
                        </label>

                        <div class="flex items-stretch gap-2">
                            <div class="inline-flex items-center justify-center px-4 rounded-2xl bg-white/5 border border-white/15 text-[15px] text-zinc-300 num-tabular">
                                +962
                            </div>
                            <input
                                id="phone"
                                name="phone"
                                type="tel"
                                inputmode="numeric"
                                autocomplete="tel"
                                placeholder="79 786 8335"
                                required
                                aria-describedby="phone-help"
                                class="flex-1 bg-white/5 border border-white/15 rounded-2xl px-4 py-3.5 text-[16px] num-tabular tracking-wide text-white placeholder:text-zinc-500 focus:outline-none focus:border-white/40 focus:bg-white/10 transition"
                            >
                        </div>

                        <button
                            type="submit"
                            class="w-full inline-flex items-center justify-center gap-2 rounded-2xl bg-white text-zinc-950 text-[15px] font-medium py-3.5 hover:bg-zinc-100 transition"
                        >
                            <span x-show="!submitted">Send me the link</span>
                            <span x-show="submitted" x-cloak class="inline-flex items-center gap-2">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>
                                Sent to your phone
                            </span>
                        </button>

                        <p id="phone-help" class="text-[12px] text-zinc-500">
                            We send a one-time code by SMS. No password, no email.
                        </p>

                        <div id="join-result" role="status" aria-live="polite"></div>
                    </form>
                </div>
            </div>
        </div>
    </section>

    {{-- ──────────────────────────────────────────
         7. FOOTER — minimal
         ────────────────────────────────────────── --}}
    <footer class="border-t border-zinc-100">
        <div class="mx-auto max-w-7xl px-6 lg:px-10 py-10 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6">

            <div class="inline-flex items-center gap-2.5">
                <span class="brand-dot" style="width: 10px; height: 10px;"></span>
                <span class="text-[14px] font-medium text-zinc-950">Dot</span>
                <span class="text-[12px] text-zinc-400 ms-3">The internet of what people actually do.</span>
            </div>

            <nav class="flex items-center gap-7 text-[13px] text-zinc-600">
                <a href="/partners" class="hover:text-zinc-950 transition">Partners</a>
                <a href="/privacy" class="hover:text-zinc-950 transition">Privacy</a>
                <a href="/terms" class="hover:text-zinc-950 transition">Terms</a>
            </nav>

            <p class="text-[12px] text-zinc-400 num-tabular">
                &copy; 2026 Dot Wallet, Amman
            </p>
        </div>
    </footer>

    {{-- ──────────────────────────────────────────
         Alpine.js controller
         ────────────────────────────────────────── --}}
    <script>
        function dotLanding() {
            return {
                scrollProgress: 0,
                pathPoint: { x: 12, y: 0 },
                _ticking: false,

                init() {
                    this.onScroll = this.onScroll.bind(this);
                    window.addEventListener('scroll', this.onScroll, { passive: true });
                    this.onScroll();
                },

                onScroll() {
                    if (this._ticking) return;
                    this._ticking = true;
                    requestAnimationFrame(() => {
                        const doc = document.documentElement;
                        const max = doc.scrollHeight - window.innerHeight;
                        const p = max > 0 ? Math.min(1, Math.max(0, window.scrollY / max)) : 0;
                        this.scrollProgress = p;

                        // Sample the SVG path at scroll progress to ride the dot along it.
                        // Cubic path mirrored from CSS — recompute roughly at runtime.
                        const t = p;
                        // Three-segment piecewise cubic approx:
                        const seg = t < 0.38 ? 0 : t < 0.68 ? 1 : 2;
                        const localT = seg === 0 ? t / 0.38 : seg === 1 ? (t - 0.38) / 0.30 : (t - 0.68) / 0.32;
                        let x, y;
                        if (seg === 0) {
                            // 12 -> 4
                            x = 12 + (4 - 12) * this._easeInOut(localT);
                            y = 0 + 380 * t;
                        } else if (seg === 1) {
                            x = 4 + (20 - 4) * this._easeInOut(localT);
                            y = 380 + (680 - 380) * localT;
                        } else {
                            x = 20 + (12 - 20) * this._easeInOut(localT);
                            y = 680 + (1000 - 680) * localT;
                        }
                        this.pathPoint = { x, y };
                        this._ticking = false;
                    });
                },

                _easeInOut(t) {
                    return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
                },

                setSpotlight(e) {
                    const r = e.currentTarget.getBoundingClientRect();
                    e.currentTarget.style.setProperty('--mx', (e.clientX - r.left) + 'px');
                    e.currentTarget.style.setProperty('--my', (e.clientY - r.top) + 'px');
                },

                clearSpotlight(e) {
                    e.currentTarget.style.setProperty('--mx', '-200px');
                    e.currentTarget.style.setProperty('--my', '-200px');
                },
            }
        }
    </script>
</body>
</html>