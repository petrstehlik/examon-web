import { WwwPage } from './app.po';

describe('www App', () => {
  let page: WwwPage;

  beforeEach(() => {
    page = new WwwPage();
  });

  it('should display welcome message', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('Welcome to app!');
  });
});
