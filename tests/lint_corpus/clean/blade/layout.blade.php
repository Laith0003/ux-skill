<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}" dir="{{ app()->getLocale() === 'ar' ? 'rtl' : 'ltr' }}">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="csrf-token" content="{{ csrf_token() }}">
    <title>@yield('title', config('app.name'))</title>
    {{-- Never ship Lorem ipsum or {{TODO}} tokens from this layout; the
         copy check in CI greps rendered pages for both. --}}
    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
<body class="min-h-dvh bg-canvas text-ink antialiased">
    <a class="skip-link" href="#main">Skip to content</a>

    <header class="site-header">
        <a href="{{ route('home') }}" class="site-header__brand">
            <img src="{{ asset('img/logo-wordmark.svg') }}" alt="{{ config('app.name') }} home" width="132" height="28">
        </a>
        <nav aria-label="{{ __('Primary') }}">
            <ul class="site-header__nav">
                <li><a href="{{ route('orders.index') }}">{{ __('Orders') }}</a></li>
                <li><a href="{{ route('customers.index') }}">{{ __('Customers') }}</a></li>
                <li><a href="{{ route('reports.index') }}">{{ __('Reports') }}</a></li>
            </ul>
        </nav>
    </header>

    <main id="main" class="page">
        @yield('content')
    </main>

    <footer class="site-footer">
        <p>&copy; {{ now()->year }} {{ config('app.name') }}. {{ __('Registered in Amman, Jordan.') }}</p>
    </footer>
</body>
</html>
