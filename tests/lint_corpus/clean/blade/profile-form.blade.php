<form method="POST" action="{{ route('profile.update') }}" class="form-grid">
    @csrf
    @method('PATCH')

    <div class="field">
        <label for="name">{{ __('Full name') }}</label>
        <input id="name" name="name" type="text" value="{{ old('name', $user->name) }}" autocomplete="name" required
               aria-describedby="@error('name') name-error @enderror">
        @error('name')
            <p id="name-error" class="field-error" role="alert">{{ $message }}</p>
        @enderror
    </div>

    <div class="field">
        <label for="phone">{{ __('Mobile number') }}</label>
        <input id="phone" name="phone" type="tel" inputmode="tel" dir="ltr" value="{{ old('phone', $user->phone) }}"
               placeholder="+962 7X XXX XXXX" autocomplete="tel">
    </div>

    <div class="field">
        <label for="language">{{ __('Interface language') }}</label>
        <select id="language" name="language">
            <option value="en" @selected($user->language === 'en')>English</option>
            <option value="ar" @selected($user->language === 'ar')>العربية</option>
        </select>
    </div>

    <div class="form-actions">
        <button type="submit" class="btn btn-primary">{{ __('Save profile') }}</button>
        <a class="btn btn-quiet" href="{{ route('dashboard') }}">{{ __('Back to dashboard') }}</a>
    </div>
</form>
