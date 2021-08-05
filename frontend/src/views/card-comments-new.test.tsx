import React from 'react';
import { Card, Comment } from '../schemas';
import { CardCommentsNewProps, CardCommentsNew } from './card-comments-new';
import { createComment } from '../utils'
import { mount } from 'enzyme';
import { act } from 'react-dom/test-utils';

jest.mock('../utils', () => {
  return {
    commentTypeToString: () => 'meow',
    createComment: jest.fn(),
  };
});

describe('<CardCommentsNew />', () => {
  describe('happy paths', () => {
    beforeEach(() => {
      createComment.mockImplementation(() => {
        return Promise.resolve();
      });
    });
    it('adds a comment', async () => {
      let called = false;
      const props: CardCommentsNewProps = {
        card<Card>: {
          id: 1,
          displayName: 'Compersion',
          name: 'compersion',
          type: 'feeling',
          level: 1,
          definition: 'meow',
          definitionSource: 'meow',
          image: {
            og: 'about:blank',
            lg: 'about:blank',
            md: 'about:blank',
          },
        },
        hasCommented: false,
        onSubmit: () => {
          called = true;
        },
      };
      const screen = mount(<CardCommentsNew {...props} />);
      const el = screen.find('textarea');
      await act(async () => {
        el.simulate("change", {
          target: { value: 'princess.wiggles' }
        })
      });
      expect(el.instance().value).toEqual('princess.wiggles');
      const submit = screen.find('button[type="submit"]');
      await act(async () => {
        await submit.simulate("click");
      });
      expect(screen.find('[role="success-info"]')).toBeTruthy();
      expect(called).toBeTruthy();
    });
  });
  describe('forlorn paths', () => {
    beforeEach(() => {
      createComment.mockImplementation(() => {
        return Promise.reject();
      });
    });
    test('handles empty comment on submit', async () => {
      let called = false;
      const props: CardCommentsNewProps = {
        card<Card>: {
          id: 1,
          displayName: 'Compersion',
          name: 'compersion',
          type: 'feeling',
          level: 1,
          definition: 'meow',
          definitionSource: 'meow',
          image: {
            og: 'about:blank',
            lg: 'about:blank',
            md: 'about:blank',
          },
        },
        hasCommented: false,
        onSubmit: () => { called = true },
      }
      const screen = mount(<CardCommentsNew {...props} />);
      const el = screen.find('textarea');
      const submit = screen.find('button[type="submit"]');
      await act(async () => {
        await submit.simulate("click");
      });
      expect(screen.find('[data-testid="nobody-error"]')).toBeTruthy();
      expect(called).toBeFalsy();
    });
    test('handles error on submit', async () => {
      let called = false;
      const props: CardCommentsNewProps = {
        card<Card>: {
          id: 1,
          displayName: 'Compersion',
          name: 'compersion',
          type: 'feeling',
          level: 1,
          definition: 'meow',
          definitionSource: 'meow',
          image: {
            og: 'about:blank',
            lg: 'about:blank',
            md: 'about:blank',
          },
        },
        hasCommented: false,
        onSubmit: () => { called = true },
      }
      const screen = mount(<CardCommentsNew {...props} />);
      const submit = screen.find('button[type="submit"]');
      await act(async () => {
        await submit.simulate("click");
      });
      expect(called).toBeFalsy();
      expect(screen.find('button[type="submit"]')).toBeTruthy();
    });
  });
});
