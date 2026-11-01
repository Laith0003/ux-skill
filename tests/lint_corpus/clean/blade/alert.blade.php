@props(['type' => 'info', 'title' => null, 'dismissible' => false])

@php
    $tones = [
        'info' => 'border-line bg-surface',
        'warning' => 'border-caution/50 bg-caution-subtle',
        'error' => 'border-critical/50 bg-critical-subtle',
    ];
    $role = $type === 'error' ? 'alert' : 'status';
@endphp

<div {{ $attributes->merge(['class' => 'alert flex gap-3 rounded-md border px-4 py-3 '.$tones[$type]]) }} role="{{ $role }}">
    <svg class="alert__icon" aria-hidden="true" viewBox="0 0 20 20" width="20" height="20">
        <circle cx="10" cy="10" r="8" fill="none" stroke="currentColor" stroke-width="1.5" />
        <path d="M10 6v5M10 13.5v.5" stroke="currentColor" stroke-width="1.5" />
    </svg>
    <div class="alert__body">
        @if ($title)
            <p class="alert__title font-medium">{{ $title }}</p>
        @endif
        <div class="alert__text">{{ $slot }}</div>
    </div>
    @if ($dismissible)
        <button type="button" class="alert__dismiss" aria-label="{{ __('Dismiss this message') }}" x-on:click="$el.closest('.alert').remove()">
            <svg aria-hidden="true" viewBox="0 0 16 16" width="16" height="16">
                <path d="M4 4l8 8M12 4l-8 8" stroke="currentColor" stroke-width="1.5" />
            </svg>
        </button>
    @endif
</div>
