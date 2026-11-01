@extends('layouts.app')

@section('title', __('Invoice :number', ['number' => $invoice->number]))

@section('content')
<article class="invoice" dir="{{ $invoice->locale === 'ar' ? 'rtl' : 'ltr' }}">
    <header class="invoice__header">
        <h1 class="invoice__title">{{ __('Invoice') }} {{ $invoice->number }}</h1>
        <p class="invoice__meta">
            {{ __('Issued') }} <time datetime="{{ $invoice->issued_at->toDateString() }}">{{ $invoice->issued_at->isoFormat('LL') }}</time>
        </p>
    </header>

    @if ($invoice->locale === 'ar')
        <p class="invoice__note" lang="ar">يرجى السداد خلال ١٤ يوماً من تاريخ الإصدار.</p>
    @endif

    <table class="invoice__lines">
        <caption class="sr-only">{{ __('Line items') }}</caption>
        <thead>
            <tr>
                <th scope="col">{{ __('Item') }}</th>
                <th scope="col" class="num">{{ __('Qty') }}</th>
                <th scope="col" class="num">{{ __('Amount') }}</th>
            </tr>
        </thead>
        <tbody>
            @foreach ($invoice->lines as $line)
                <tr>
                    <td>{{ $line->description }}</td>
                    <td class="num">{{ $line->quantity }}</td>
                    <td class="num">{{ $line->amount->format() }}</td>
                </tr>
            @endforeach
        </tbody>
        <tfoot>
            <tr>
                <th scope="row" colspan="2">{{ __('Total due') }}</th>
                <td class="num">{{ $invoice->total->format() }}</td>
            </tr>
        </tfoot>
    </table>

    <a class="btn btn-primary" href="{{ route('invoices.pdf', $invoice) }}" download>
        {{ __('Download PDF') }}
    </a>
</article>
@endsection
